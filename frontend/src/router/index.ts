import { createWebHistory, createRouter } from 'vue-router'
import {useMainStore} from "../store/main-store";

const  routes = [
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
                ],
            },
        ],
    },
    {
        path: '/:not_found_path(.*)', redirect: '/main',
    },
];


const router = createRouter({
    history: createWebHistory(),
    base: import.meta.env.BASE_URL,
    routes, //same --- > routes:routes
});

router.beforeEach(async (to, from) => {
    if(to.name !=='login')
    {
        const store = useMainStore();
        await store.actionCheckLoggedIn();
    }
});

router.afterEach(async (to, from) => {
    if(to.name !=='login')
    {
        const store = useMainStore();
        await store.actionCheckLoggedIn();
    }
});

export default router;