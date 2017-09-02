import schema
import pytest

def test_repr():
	assert repr(schema.Team())
	assert repr(schema.User())
	assert repr(schema.Challenge())
	assert repr(schema.Submission())