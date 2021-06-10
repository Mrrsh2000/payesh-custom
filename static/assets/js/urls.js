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


////////////////// LOG //////////////////

//   // API URLS:
const LOG_API_DATATABLE_URL = API_VERSION + 'logs/datatable/';

////////////////// SELECT2 //////////////////
