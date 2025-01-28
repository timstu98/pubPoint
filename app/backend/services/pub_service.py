from algorithms.pub_finder.suggest_pub import suggest_pub
from models import User, Pub, UserGroupQuery


def suggest_pub_for_group(group_id: str, algorithm="geo-centre") -> Pub:
    """
    Service to coordinate optimal pub calculation
    """
    # Get users in group
    users = User.query.join(UserGroupQuery).filter(UserGroupQuery.group_id == group_id).all()

    # Get all pubs
    pubs = Pub.query.all()

    # Find optimal pub
    return suggest_pub(users, pubs, algorithm)
