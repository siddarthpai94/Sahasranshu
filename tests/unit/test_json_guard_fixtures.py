import json
from pathlib import Path

from sahasranshu.llm.json_guard import parse_json_response


def load_fixtures():
    p = Path("tests/fixtures/gemini_raw_responses.json")
    return json.loads(p.read_text())


def test_parse_various_raw_responses():
    fixtures = load_fixtures()

    # stance valid
    result = parse_json_response(fixtures["stance_valid"]["raw"])
    assert result == fixtures["stance_valid"]["expected"]

    # malformed trailing comma repaired
    result2 = parse_json_response(fixtures["stance_malformed_trailing_comma"]["raw"])
    assert result2 == fixtures["stance_malformed_trailing_comma"]["expected"]

    # array of hypotheses
    result3 = parse_json_response(fixtures["hypotheses_array_inline"]["raw"])
    assert result3 == fixtures["hypotheses_array_inline"]["expected"]

    # wrapped codeblock
    result4 = parse_json_response(fixtures["wrapped_with_text_and_codeblock"]["raw"])
    assert result4 == fixtures["wrapped_with_text_and_codeblock"]["expected"]
