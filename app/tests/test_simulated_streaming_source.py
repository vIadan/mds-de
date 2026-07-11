from app.sources.simulate import SimulatedMessageSource
from app.models.message import Message

def test_simulated_message_source_yield():
    source = SimulatedMessageSource()
    gen = source.stream()
    message = next(gen)

    assert isinstance(message, Message)