import { writable } from 'svelte/store';

function createAuthStore() {
    // Don't access localStorage during module initialization
    const { subscribe, set, update } = writable({
        token: null,
        user: null,
        isAuthenticated: false
    });

    return {
        subscribe,
        login: (token, user) => {
            localStorage.setItem('token', token);
            set({ token, user, isAuthenticated: true });
        },
        logout: () => {
            localStorage.removeItem('token');
            set({ token: null, user: null, isAuthenticated: false });
        },
        setUser: (user) => {
            update(state => ({ ...state, user, isAuthenticated: true }));
        },
        // Call this method to initialize from localStorage
        init: () => {
            const token = localStorage.getItem('token');
            if (token) {
                update(state => ({ ...state, token }));
                return token;
            }
            return null;
        }
    };
}

export const authStore = createAuthStore();
