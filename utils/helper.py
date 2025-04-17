from django.db.models import Sum, Case, When, IntegerField


def get_vote_score_expr(value_field='vote__value'):
    return Sum(
        Case(
            When(**{value_field: 1}, then=1),
            When(**{value_field: -1}, then=-1),
            default=0,
            output_field=IntegerField(),
        )
    )
