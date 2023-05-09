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
                    // {
                    //     path: 'profile',
                    //     component: RouterComponent,
                    //     redirect: 'profile/view',
                    //     children: [
                    //         {
                    //             path: 'view',
                    //             component: () => import(
                    //                 /* webpackChunkName: "main-profile" */ './views/main/profile/UserProfile.vue'),
                    //         },
                    //         {
                    //             path: 'edit',
                    //             component: () => import(
                    //                 /* webpackChunkName: "main-profile-edit" */ './views/main/profile/UserProfileEdit.vue'),
                    //         },
                    //         {
                    //             path: 'password',
                    //             component: () => import(
                    //                 /* webpackChunkName: "main-profile-password" */ './views/main/profile/UserProfileEditPassword.vue'),
                    //         },
                    //     ],
                    // },
                    // {
                    //     path: 'admin',
                    //     component: () => import(/* webpackChunkName: "main-admin" */ './views/main/admin/Admin.vue'),
                    //     redirect: 'admin/users/all',
                    //     children: [
                    //         {
                    //             path: 'users',
                    //             redirect: 'users/all',
                    //         },
                    //         {
                    //             path: 'users/all',
                    //             component: () => import(
                    //                 /* webpackChunkName: "main-admin-users" */ './views/main/admin/AdminUsers.vue'),
                    //         },
                    //         {
                    //             path: 'users/edit/:id',
                    //             name: 'main-admin-users-edit',
                    //             component: () => import(
                    //                 /* webpackChunkName: "main-admin-users-edit" */ './views/main/admin/EditUser.vue'),
                    //         },
                    //         {
                    //             path: 'users/create',
                    //             name: 'main-admin-users-create',
                    //             component: () => import(
                    //                 /* webpackChunkName: "main-admin-users-create" */ './views/main/admin/CreateUser.vue'),
                    //         },
                    //     ],
                    // },
                ],
            },
        ],
    },
    {
        path: '/:not_found_path(.*)', redirect: '/',
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