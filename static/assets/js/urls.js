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


////////////////// Data //////////////////

//   // API URLS:
const WATER_API_DELETE_URL = API_VERSION + 'water/0',
    WATER_API_UPDATE_URL = API_VERSION + 'water/0',
    WATER_API_DATATABLE_URL = API_VERSION + 'water/datatable/',
    WATER_API_CREATE_URL = API_VERSION + 'water/';


//  // TEMPLATE URLS:
const
    WATER_CREATE_TEMPLATE = '/data/water/create',
    WATER_UPDATE_TEMPLATE = '/data/water/update/0',
    WATER_LIST_TEMPLATE = '/data/water/list';


////////////////// LOG //////////////////

//   // API URLS:
const LOG_API_DATATABLE_URL = API_VERSION + 'logs/datatable/';

////////////////// SELECT2 //////////////////

const
    SELECT2_CITY = API_VERSION + 'select2/city',
    SELECT2_PART = API_VERSION + 'select2/part',
    SELECT2_TOWN = API_VERSION + 'select2/town',
    SELECT2_VILLAGE = API_VERSION + 'select2/village',
    SELECT2_EXCEL = API_VERSION + 'select2/excel',
    SELECT2_SEASON = API_VERSION + 'select2/season';


////////////////// SELECT2 STR //////////////////

const
    SELECT2_REPLACE_TANKER_STR = API_VERSION + 'select2/replace_tanker_str',
    SELECT2_CUSTOM_WATER_NEED_STR = API_VERSION + 'select2/custom_water_need_str',
    SELECT2_HOUSE_SOURCE_NEED_STR = API_VERSION + 'select2/house_source_need_str',
    SELECT2_WATER_NETWORK_NEED_STR = API_VERSION + 'select2/water_network_need_str'

;
