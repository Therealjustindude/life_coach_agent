from app.agent.react_prompt_builder import ReactPromptBuilder

def test_tools_section_included():
    b = ReactPromptBuilder(coach_style="default", include_examples=False)
    p = b.build_prompt(context=None, user_input="hi", tools_guide="- now → Returns UTC time")
    assert "Available Tools:" in p and "now" in p

def test_omits_empty_context():
    b = ReactPromptBuilder(coach_style="default", include_examples=False)
    p = b.build_prompt(context="", user_input="hi")
    assert "Context:" not in p