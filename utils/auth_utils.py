from utils.db_utils import get_account_holder

def login(user_id):
    """
    Verifies if the user can access the system
    input:
        user_id: bank or a user's id
    output:
        json {"status": <status code>, "error_message": <error message>, "access_level": <access level>}
    """
    
    output = {"status": "200", "error_message": None, "access_level": None}
    user_id_str = str(user_id)
    if user_id_str.isalpha() and user_id.upper() == "BANK":
        output["access_level"] = "B"
    elif user_id_str.isdigit() and user_exists(user_id):
        output["access_level"] = "U"
    else:
        output["status"] = "404"
        output["error_message"] = "User not found"
    
    return output

def user_exists(user_id):
    """
    Verifies if the user exists in the system
    input:
        user_id: user's id
        engine: (Optional) db connection
    output:
        boolean
    """
    
    account_holder = get_account_holder(user_id)
    if len(account_holder) > 0:
        return True
    else:
        return False

                    