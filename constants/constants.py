# Права, которые влияют на функционал в ПП
proposal_rights = ['DIRECTOR-EX', 'EXPERT-EX']

# Конечные вердикты по ПП, которые выносит руководитель исполнительной дирекции
final_proposal_verdict_list = ['SUCCESS', 'REJECT', 'REVIEW', 'EXPERTS_EVALUATE', 'DIRECTOR_EVALUATE',
                               'ARCHIVED']

# Вердикты по ПП, которые выносит каждый эксперт после проверки
expert_verdict_list = ['SUCCESS', 'REJECT']

# Приоритет проекта
project_priority_list = ['HIGH', 'NORMAL']

# Статусы проектов
project_status_list = ['INITIATION', 'PREPARATION', 'REALIZATION', 'COMPLETION',
                       'POST_PROJECT_MONITORING', 'ARCHIVED', 'CANCELED']

# тип оценки показателя
indicator_evaluation_list = ['INCREASING', 'DECREASING', 'FIXED']

# Охват единиц совокупности
coverage_list = ['SELECTIVE', 'MONOGRAPHIC', 'CONTINUOUS', 'MAIN_ARRAY']

# Статусы для значений показателей
indicator_status_list = ['AWAITING', 'ACHIEVED', 'DISRUPTION']

# Статусы контрактов
contracts_status_list = ['INITIATION', 'DOC_PREPARED', 'COMPETITIVE_PROCEDURES', 'SIGNING', 'EXECUTED']

# Статусы результатов проекта
project_result_status_list = ['IN_PROGRESS', 'COMPLETED', 'ACHIEVED', 'CANCELED']

# Форматы документов
DOCUMENT_EXT = ['.docx', '.doc', '.txt', '.pptx', '.ppt', '.pdf']

# Форматы архивов
ARCHIVE_EXT = ['.rar', '.zip', '.7z']

CALENDAR_PLAN_STATUS = ['IN_WORK', 'COMPLETE', 'CONFIRMED', 'OVERDUE', 'FORECAST_FAILURE']

backpack_table_list = ['MAIN', 'SET_USER_ROLE', 'REMOVE_USER_ROLE']

project_log_list = ['UPDATE', 'SET_USER_ROLE', 'REMOVE_USER_ROLE', 'DELETE']

project_indicator_log_list = ['UPDATE', 'DELETE', 'SET_USER_ROLE', 'REMOVE_USER_ROLE', 'UPDATE_VALUE', 'DELETE_VALUE']

project_indicator_value_log_list = ['UPDATE_VALUE', 'DELETE_VALUE', 'CREATE_VALUE']

project_file_log_list = ['UPLOAD', 'REMOVE']

budget_costs_list = ['WAGE', 'OVERHEADS', 'EQUIPMENT', 'SOFTWARE', 'CONSUMABLES', 'BUSINESS_TRIPS', 'EDUCATION']

calendar_plan_dict = {
    'STAGE': 'Этап',
    'WORK': 'Работа',
    'CONTROL_POINT': 'Контрольная точка',
    'PREPARATION': 'Контрольная точка',
    'INITIATION': 'Контрольная точка',
    'REALIZATION': 'Контрольная точка'
}
