import jsonschema

schema = {
    "$schema": "http://json-schema.org/draft/2019-09/schema#",
    "title": "Schema for grading a student answer that must be a similar value to the correct answer.",
    "type": "object",
    "properties": {
        "student_answer": {"type": "number"},
        "correct_answer": {"type": "number"},
        "tolerance": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["percentage", "absolute"]
                },
                "value": {"type": "number"}
            }
        }
    },
    "additionalProperties": False
}

def is_valid(instance, schema):
    return jsonschema.Draft7Validator(schema).is_valid(instance)

def absolute_error(student_answer, correct_answer):
    return abs(student_answer - correct_answer)

def percent_error(student_answer, correct_answer):
    return 100 * abs(student_answer - correct_answer) / correct_answer

def assert_similar(student_answer, correct_answer, tolerance):
    if tolerance["type"] == "absolute":
        error = absolute_error(student_answer, correct_answer)
    else:
        error = percent_error(student_answer, correct_answer)

    return error <= tolerance["value"]

def handler(event, context):
    if "body" not in event:
        return {"error": "request has no body"}
    elif not is_valid(event["body"], schema):
        return {"error": "body threw a schema error."}
    else:
        body = event["body"]

        student_answer = body["student_answer"]
        correct_answer = body["correct_answer"]
        tolerance = body["tolerance"]

        return {
            "is_correct": assert_similar(student_answer, correct_answer, tolerance)
        }

if __name__ == "__main__":
    from pprint import pprint

    event = {
        "body": {
            "student_answer": 3,
            "correct_answer": 3.5,
            "tolerance": {
                "type": "percentage",
                "value": 20
            }
        }
    }

    pprint(event)
    pprint(handler(event, {}))
    