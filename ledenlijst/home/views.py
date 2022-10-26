from django.shortcuts import render
import datetime
from home.models import Member
import csv, io
from django.http import HttpResponse
from django.core.exceptions import ValidationError

# Create your views here.

TEMPLATE_DIRS = 'os.path.join(BASE_DIR, "templates"),'


def index(request):
    return render(request, "index.html")


def upload_csv(request):
    if not request.FILES["csv_file"]:
        return render_result_message(request, "Geen bestand geselecteerd")
    csv_file = request.FILES["csv_file"]
    if not csv_file.name.endswith(".csv"):
        return render_result_message(request, "Bestand is niet van CSV type")
    if csv_file.multiple_chunks():
        return render_result_message(request, "Bestand te groot")
    try:
        data_set = csv_file.read().decode("utf-8")
        io_string = io.StringIO(data_set)
        members = read_members_from_csv_file(io_string)
    except Exception as e:
        print(request, "Unable to upload file. " + repr(e))

    (
        existing_members,
        invalid_email_members,
        created_members_counter,
    ) = add_member_to_database(members)

    result = f"""{created_members_counter} nieuwe leden geimporteerd.
{len(existing_members)} reeds bestaande leden genegeerd
Onjuiste emails: {len(invalid_email_members)}\n\n"""
    for lid in existing_members:
        result += f"Bestaande: {lid.email}\n"
    for lid in invalid_email_members:
        result += f"Email onjuist: {lid.email}\n"
    return render_result_message(request, result)


def render_result_message(request, message):
    return render(request, "index.html", {"result": message})


def add_member_to_database(members):
    existing_members = []
    invalid_email_members = []
    created_members_counter = 0
    for member in members:
        try:
            member.validate_unique()
        except ValidationError:
            existing_members.append(member)
            continue
        try:
            member.full_clean()
        except ValidationError:
            invalid_email_members.append(member)
            continue
        member.save()
        created_members_counter += 1

    return existing_members, invalid_email_members, created_members_counter


def read_members_from_csv_file(io_string):
    members = []
    for column in csv.reader(io_string):
        if not column[0] or not column[1] or not column[2]:
            continue
        firstname = column[0]
        lastname = column[1]
        email = column[2]

        # Check for header
        if firstname == "voornaam" and lastname == "achternaam" and email == "email":
            continue
        members.append(Member(firstname, lastname, email))
    return members
