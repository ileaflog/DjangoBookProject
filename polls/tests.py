import datetime
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from polls.models import Poll, Choice

# Create your tests here.

CHOICE_TEXT = "A poll choice"

class PollMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        :return:
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for polls whose pub_date
        is older than 1 day
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=2))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return True for polls whose pub_date
        is within the last day
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)


def create_poll(question, days, choice_text=CHOICE_TEXT):
    """
    Creates a poll with the given 'question' published the given number of
    'days' offset to now (negative for polls published in the past,
    positive for polls that have yet to be published).
    """
    now = timezone.now()
    result = Poll(question=question, pub_date=now + datetime.timedelta(days))
    result.save()

    if choice_text:
        choice = Choice(choice_text=choice_text, poll=result)
        choice.save()

    return result


class PollViewTests(TestCase):
    LATEST_POLL_LIST = "latest_poll_list"

    def test_index_view_with_no_polls(self):
        """
        If no polls exist, an appropriate message should be returned.
        :return:
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context[PollViewTests.LATEST_POLL_LIST], [])

    def test_index_view_with_a_past_poll_no_choices(self):
        """
        We'll create a poll with no choices an ensure that it does not show up in the index.
        """
        create_poll(question="No choices.", days=-10, choice_text=None)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context[PollViewTests.LATEST_POLL_LIST], [])

    def test_index_view_with_a_past_poll(self):
        p = create_poll(question="Past polly.", days=-10, choice_text="A test choice.")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context[PollViewTests.LATEST_POLL_LIST], ['<Poll: Past polly.>'])

    def test_index_view_with_a_future_poll(self):
        """
        Polls with a pub_date in the future should not be displayed on the
        index page.
        """
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.", status_code=200)
        self.assertQuerysetEqual(response.context[PollViewTests.LATEST_POLL_LIST], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        """
        Even if both past and future polls exist, only past polls should be
        displayed.
        """
        create_poll(question="Past poll.", days=-30, )
        create_poll(question="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context[PollViewTests.LATEST_POLL_LIST], ['<Poll: Past poll.>'])

    def test_index_view_with_two_past_polls(self):
        """
        The polls index page may display multiple polls.
        """
        create_poll(question="Past poll 1.", days=-30)
        create_poll(question="Past poll 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context[PollViewTests.LATEST_POLL_LIST],
                ['<Poll: Past poll 2.>', '<Poll: Past poll 1.>']
        )


class PollDetailTests(TestCase):
    def test_detail_view_with_a_future_poll(self):
        future_poll = create_poll(question="Is it 2020 yet?", days=30)
        response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_poll(self):
        POLL_QUESTION = "This poll was published?"
        past_poll = create_poll(question=POLL_QUESTION, days=-15)
        response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response=response, text=(POLL_QUESTION), status_code=200, html=False)