export interface IUserProfile {
    email: string;
    is_active: boolean;
    roles: string;
    full_name: string;
    id: number;
}

export interface MainState {
    token: string;
    userProfile: IUserProfile | null;
}

export interface AdminState {
    users: IUserProfile[];
}

