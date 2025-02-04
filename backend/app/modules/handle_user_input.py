# app\modules\handle_user_input.py

from app.modules.operation import (
    Calculate,
    Predict,
    Compare,
    Analyze,
    CheckYear,
    CheckEntity,
    CheckMeasures,
    CheckOperation,
)

#! Entry point for Operation Classes


# 1. Validate user input for important keywords
def validate_user_input(extracted_keywords):

    # * Call the Class - CheckOperation
    operation = CheckOperation(extracted_keywords)
    validation_result = operation.check()
    if validation_result:
        print(validation_result)
        return validation_result  # Early exit if validation fails

    # * Call the Class - CheckTimePeriod
    time_period = CheckYear(extracted_keywords)
    validation_result = time_period.check()
    if validation_result:
        print(validation_result)
        return validation_result

    # * Call the Class - CheckEntity
    entity = CheckEntity(extracted_keywords)
    validation_result = entity.check()
    if validation_result:
        print(validation_result)
        return validation_result

    # * Call the Class - CheckMeasures
    measure = CheckMeasures(extracted_keywords)
    validation_result = measure.check()
    if validation_result:
        print(validation_result)
        return validation_result

    print("Validation passed.")
    return None


def handle_user_input(extracted_keywords, data):

    # Determine the operation (Calculate, Predict, etc.)
    user_operation = extracted_keywords["operation"]

    if "calculate" in user_operation:
        operation = Calculate(extracted_keywords, data)
        operation_response = operation.process()
        return operation_response

    elif "predict" in user_operation:
        operation = Predict(extracted_keywords, data)
        operation_response = operation.process()
        print("This is a Predict")
        return operation_response

    # # elif "compare" in user_operation:
    # #     operation = Compare(extracted_keywords)
    # #     print("This is a Compare")

    # # elif "analyze" in user_operation:
    # #     operation = Analyze(extracted_keywords)
    # #     print("This is a Analyze")

    else:
        return f"Error: Unrecognized operation '{user_operation}'"
