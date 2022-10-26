from django.test import TestCase
from home.models import Member
from home.views import add_member_to_database
from django.core.exceptions import ObjectDoesNotExist

# Create your tests here.


class CreateMembersTestCase(TestCase):
    def test_create_member(self):
        (
            existing_members,
            invalid_email_members,
            created_members_counter,
        ) = add_member_to_database(
            [Member("test firstname", "test lastname", "testemail@email.email")]
        )
        member = Member.objects.get(
            firstname="test firstname",
            lastname="test lastname",
            email="testemail@email.email",
        )
        self.assertEqual(member.firstname, "test firstname")
        self.assertEqual(member.lastname, "test lastname")
        self.assertEqual(member.email, "testemail@email.email")
        self.assertEqual(existing_members, [])
        self.assertEqual(invalid_email_members, [])
        self.assertEqual(created_members_counter, 1)

    def test_create_member_invalid_email(self):
        (
            existing_members,
            invalid_email_members,
            created_members_counter,
        ) = add_member_to_database(
            [Member("test firstname", "test lastname", "invalid email")]
        )
        with self.assertRaises(ObjectDoesNotExist):
            Member.objects.get(
                firstname="test firstname",
                lastname="test lastname",
                email="invalid email",
            )
        self.assertEqual(existing_members, [])
        self.assertEqual(
            invalid_email_members,
            [
                Member(
                    firstname="test firstname",
                    lastname="test lastname",
                    email="invalid email",
                )
            ],
        )
        self.assertEqual(created_members_counter, 0)

    def test_create_member_already_exists(self):
        Member(
            firstname="test firstname",
            lastname="test lastname",
            email="testemail@email.email",
        ).save()
        (
            existing_members,
            invalid_email_members,
            created_members_counter,
        ) = add_member_to_database(
            [Member("test firstname", "test lastname", "testemail@email.email")]
        )
        with self.assertRaises(ObjectDoesNotExist):
            Member.objects.get(
                firstname="test firstname",
                lastname="test lastname",
                email="invalid email",
            )
        self.assertEqual(
            existing_members,
            [
                Member(
                    firstname="test firstname",
                    lastname="test lastname",
                    email="testemail@email.email",
                )
            ],
        )
        self.assertEqual(invalid_email_members, [])
        self.assertEqual(created_members_counter, 0)

        # Als ik meer tijd had zou ik hier meer tests toevoegen die ook de array mee geeft aan add_member_to_database
