export interface IUserProfile {
    email: string;
    is_active: boolean;
    roles: string;
    full_name: string;
    id: number;
}

export interface MainState {
    token: string | undefined;
    userProfile: IUserProfile | null;
    isLoading: boolean;
}

export interface AdminState {
    users: IUserProfile[];
}

