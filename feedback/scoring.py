def make_probability(prediction_result):
    return prediction_result.probability[1] * 100


def score(prediction_result):
    return round(make_probability(prediction_result))
