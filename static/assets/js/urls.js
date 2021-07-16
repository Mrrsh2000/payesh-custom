////////////////// BASE URLS //////////////////
const API_VERSION = '/api/v1/',
    REFRESH_TOKEN_URL = API_VERSION + 'token/refresh/',
    LOGIN_URL = '/login/',
    CURRENT_URL = window.location.search;

////////////////// USER //////////////////

//   // API URLS:
const USER_API_DELETE_URL = API_VERSION + 'user/0',
    USER_API_UPDATE_URL = API_VERSION + 'user/0',
    SELF_API_UPDATE_URL = API_VERSION + 'user/self/',
    USER_API_DATATABLE_URL = API_VERSION + 'user/datatable/',
    USER_API_CREATE_URL = API_VERSION + 'user/';


//  // TEMPLATE URLS:
const
    USER_UPDATE_TEMPLATE = '/user/update/0',
    USER_LIST_TEMPLATE = '/user/list';


////////////////// STUDENT //////////////////

//   // API URLS:
const STUDENT_API_DELETE_URL = API_VERSION + 'student/0',
    STUDENT_API_UPDATE_URL = API_VERSION + 'student/0',
    STUDENT_API_DATATABLE_URL = API_VERSION + 'student/datatable/',
    STUDENT_API_CREATE_URL = API_VERSION + 'student/';


//  // TEMPLATE URLS:
const
    STUDENT_UPDATE_TEMPLATE = '/user/student/update/0',
    STUDENT_LIST_TEMPLATE = '/user/student/list';



////////////////// TICKET //////////////////

//   // API URLS:
const TICKET_API_DELETE_URL = API_VERSION + 'ticket/0',
    TICKET_API_UPDATE_URL = API_VERSION + 'ticket/0',
    TICKET_API_DATATABLE_URL = API_VERSION + 'ticket/datatable/',
    TICKET_API_CREATE_URL = API_VERSION + 'ticket/';


//  // TEMPLATE URLS:
const
    TICKET_UPDATE_TEMPLATE = '/ticket/ticket/update/0',
    TICKET_LIST_TEMPLATE = '/ticket/ticket/list';


////////////////// PROJECT //////////////////

//   // API URLS:
const PROJECT_API_DELETE_URL = API_VERSION + 'project/0',
    PROJECT_API_UPDATE_URL = API_VERSION + 'project/0',
    PROJECT_API_NUMBER_URL = API_VERSION + 'project/number/0',
    PROJECT_API_EDUCATION_TOGGLE_URL = API_VERSION + 'project/edu_toggle/0',
    PROJECT_API_DATATABLE_URL = API_VERSION + 'project/datatable/',
    PROJECT_API_CREATE_URL = API_VERSION + 'project/';


//  // TEMPLATE URLS:
const
    PROJECT_UPDATE_TEMPLATE = '/project/update/0',
    PROJECT_LIST_TEMPLATE = '/project/list';


////////////////// LOG //////////////////

//   // API URLS:
const LOG_API_DATATABLE_URL = API_VERSION + 'logs/datatable/';

////////////////// SELECT2 //////////////////
