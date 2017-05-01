from framework.base_user import db_session, Statistics

rm = Rm()
    # фильтруем задачи по значению updated_on
    tasks = rm.redmine.issue.filter(updated_on=datetime.today().strftime('=%Y-%m-%d'), include='journals')

    text = '<b>Время на тестирование задач ({}):</b>\n\n'.format(username)

    # Перебираем задачи, возвращаем время по статусу config['redmine']['status_in_qa_id'] за сегодня
    for task in tasks:
        time_in_qa = get_time_by_status(
            config['redmine']['status_in_qa_id'],
            task.journals.resources,
            day=datetime.today(),
            update_author=username
        )
        if time_in_qa:

            task_id = None
            resolved_time = None

            st = Statistics(user_name='Anna K', issue=task_id, time_issue=resolved_time, day=None)

            db_session.add(st)
            db_session.commit()
