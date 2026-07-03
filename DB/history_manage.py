from DB.db_setup import get_db,History

def get_history(username):
    session=get_db()
    data_history=session.query(History)\
        .filter(History.username==username)\
        .order_by(History.id.desc())\
        .limit(5)\
        .all()
    session.close()

    data_history=data_history[::-1]

    return "\n".join([f"{i.role}: {i.message}"
                      for i in data_history])


def save_history(username,role,message):
    session=get_db()
    try:
        new_history=History(username=username,role=role,message=message)
        session.add(new_history)
        session.commit()

    except Exception as e:
            session.rollback()
            return{f"status":"error","pesan":f"gagal menyimpan history: {str(e)}"}
    finally:
         session.close()

print(get_history('billy'))

