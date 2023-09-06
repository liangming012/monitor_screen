import { createWebHistory, createRouter } from 'vue-router'
import {useMainStore} from "../store/main-store";
import * as VueRouter from 'vue-router';

export const routes: VueRouter.RouteRecordRaw[] = [
    {
        path: '/',
        name: 'index',
        redirect: '/login',
        children: [
            {
                path: '/login',
                name: 'login',
                meta: {
                    title: '登录'
                },
                component: () => import('../views/Login.vue')
            },
            {
                name: 'main',
                path: 'main',
                meta: {
                    title: '首页'
                },
                component: () => import('../views/main/Main.vue'),
                redirect: '/main/dashboard',
                children: [
                    {
                        name: 'dashboard',
                        path: 'dashboard',
                        component: () => import('../views/main/Dashboard.vue'),
                    },
                    {
                        path: 'profile',
                        name: 'profile',
                        redirect: 'main/profile/view',
                        children: [
                            {
                                path: 'view',
                                name: 'profileView',
                                component: () => import('../views/main/profile/UserProfile.vue'),
                            },
                            {
                                path: 'edit',
                                name: 'profileEdit',
                                component: () => import('../views/main/profile/UserProfileEdit.vue'),
                            },
                            {
                                path: 'password',
                                name: 'profilePassword',
                                component: () => import('../views/main/profile/UserProfilePassword.vue'),
                            },
                        ],
                    },
                    {
                        path: 'user',
                        name: 'user',
                        redirect: 'main/user/list',
                        children: [
                            {
                                path: 'list',
                                name: 'users',
                                component: () => import('../views/main/user/Users.vue'),
                            },
                            {
                                path: 'edit/:id',
                                name: 'editUser',
                                component: () => import('../views/main/user/EditUser.vue'),
                                props: true,
                            },
                            {
                                path: 'add',
                                name: 'addUser',
                                component: () => import('../views/main/user/AddUser.vue'),
                            },
                        ],
                    },
                    {
                        path: 'project',
                        name: 'project',
                        redirect: '/main/project/list',
                        children: [
                            {
                                path: 'list',
                                name: 'projects',
                                component: () => import('../views/main/project/Projects.vue'),
                            },
                            {
                                path: 'edit/:id',
                                name: 'editProject',
                                component: () => import('../views/main/project/EditProject.vue'),
                                props: true,
                            },
                            {
                                path: 'add',
                                name: 'addProject',
                                component: () => import('../views/main/project/AddProject.vue'),
                            },
                        ],
                    },
                    {
                        path: 'record',
                        name: 'record',
                        redirect: '/main/record/list',
                        children: [
                            {
                                path: 'list',
                                name: 'records',
                                component: () => import('../views/main/record/Records.vue'),
                            },
                            {
                                path: 'edit/:id',
                                name: 'editRecord',
                                component: () => import('../views/main/record/EditRecord.vue'),
                                props: true,
                            },
                            {
                                path: 'add',
                                name: 'addRecord',
                                component: () => import('../views/main/record/AddRecord.vue'),
                            },
                        ],
                    },
                    {
                        path: 'screen',
                        name: 'screen',
                        redirect: '/main/screen/list',
                        children: [
                            {
                                path: 'list',
                                name: 'screens',
                                component: () => import('../views/main/screen/Screens.vue'),
                            },
                            {
                                path: 'edit/:id',
                                name: 'editScreen',
                                component: () => import('../views/main/screen/EditScreen.vue'),
                                props: true,
                            },
                            {
                                path: 'add',
                                name: 'addScreen',
                                component: () => import('../views/main/screen/AddScreen.vue'),
                            },
                        ],
                    },
                    {
                        path: 'show',
                        name: 'show',
                        redirect: '/main/show/list',
                        children: [
                            {
                                path: 'list',
                                name: 'shows',
                                component: () => import('../views/main/show/Shows.vue'),
                            },
                            {
                                path: 'edit/:id',
                                name: 'editShow',
                                component: () => import('../views/main/show/EditShow.vue'),
                                props: true,
                            },
                            {
                                path: 'add',
                                name: 'addShow',
                                component: () => import('../views/main/show/AddShow.vue'),
                            },
                        ],
                    },
                    {
                        path: 'notice',
                        name: 'notice',
                        redirect: '/main/notice/list',
                        children: [
                            {
                                path: 'list',
                                name: 'notices',
                                component: () => import('../views/main/notice/Notices.vue'),
                            },
                            {
                                path: 'edit/:id',
                                name: 'editNotice',
                                component: () => import('../views/main/notice/EditNotice.vue'),
                                props: true,
                            },
                            {
                                path: 'add',
                                name: 'addNotice',
                                component: () => import('../views/main/notice/AddNotice.vue'),
                            },
                        ],
                    },
                ],
            },
            {
                path: '/view/:id',
                name: 'view',
                meta: {
                    title: '前台屏幕'
                },
                component: () => import('../views/View.vue')
            },
        ],
    },
    {
        path: '/:not_found_path(.*)', redirect: '/main',
    },
];


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: routes, //same --- > routes:routes
});

router.beforeEach(async (to, from) => {
    if(to.name !=='login' && to.name !=='view')
    {
        const store = useMainStore();
        await store.actionCheckLoggedIn();
    }
});

router.afterEach(async (to, from) => {
    if(to.name !=='login' && to.name !=='view')
    {
        const store = useMainStore();
        await store.actionCheckLoggedIn();
        store.changeActiveMenu(router.currentRoute.value.path);
    }
});

export default router;