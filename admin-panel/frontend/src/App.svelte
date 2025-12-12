<script>
    import { onMount } from 'svelte';
    import { authStore } from './stores/auth';
    import { api } from './lib/api';
    import Login from './lib/Login.svelte';
    import Signup from './lib/Signup.svelte';
    import Admin from './lib/Admin.svelte';

    let currentPage = 'login';
    let authState;
    let isInitializing = true; // ← Add this flag

    authStore.subscribe(value => {
        authState = value;
    });

    onMount(async () => {
        console.log('=== App.svelte mounted ===');
        
        const token = localStorage.getItem('token');
        console.log('Token from localStorage:', token ? token.substring(0, 20) + '...' : 'NO TOKEN');
        
        if (token) {
            try {
                console.log('Attempting to fetch user with token...');
                const user = await api.getMe();
                console.log('User fetched successfully:', user);
                
                authStore.login(token, user);
                
                // Set page based on user role and hash
                const hash = window.location.hash.slice(1);
                if (hash === '/admin' && user.role === 'admin') {
                    currentPage = 'admin';
                } else if (hash === '/teacher' && user.role === 'teacher') {
                    currentPage = 'teacher';
                } else if (hash === '/student' && user.role === 'student') {
                    currentPage = 'student';
                } else {
                    // Default page based on role
                    if (user.role === 'admin') {
                        currentPage = 'admin';
                        window.location.hash = '/admin';
                    } else if (user.role === 'teacher') {
                        currentPage = 'teacher';
                        window.location.hash = '/teacher';
                    } else if (user.role === 'student') {
                        currentPage = 'student';
                        window.location.hash = '/student';
                    }
                }
            } catch (err) {
                console.error('Token validation failed:', err);
                localStorage.removeItem('token');
                authStore.logout();
                window.location.hash = '';
                currentPage = 'login';
            }
        } else {
            console.log('No token found, showing login');
            const hash = window.location.hash.slice(1);
            currentPage = hash === '/signup' ? 'signup' : 'login';
        }

        // Mark initialization as complete
        isInitializing = false;
        console.log('✅ Initialization complete, currentPage:', currentPage);

        // Now set up hash change listener
        window.addEventListener('hashchange', handleHashChange);

        return () => {
            window.removeEventListener('hashchange', handleHashChange);
        };
    });

    function handleHashChange() {
        // Don't handle hash changes during initialization
        if (isInitializing) {
            console.log('⏳ Still initializing, ignoring hash change');
            return;
        }

        const hash = window.location.hash.slice(1);
        console.log('Hash changed to:', hash);
        
        if (authState.isAuthenticated) {
            if (hash === '/admin' && authState.user?.role === 'admin') {
                currentPage = 'admin';
            } else if (hash === '/teacher' && authState.user?.role === 'teacher') {
                currentPage = 'teacher';
            } else if (hash === '/student' && authState.user?.role === 'student') {
                currentPage = 'student';
            } else if (hash === '/dashboard') {
                currentPage = 'dashboard';
            } else {
                // Default page based on role
                if (authState.user?.role === 'admin') {
                    currentPage = 'admin';
                    window.location.hash = '/admin';
                } else if (authState.user?.role === 'teacher') {
                    currentPage = 'teacher';
                    window.location.hash = '/teacher';
                } else if (authState.user?.role === 'student') {
                    currentPage = 'student';
                    window.location.hash = '/student';
                }
            }
        } else {
            if (hash === '/signup') {
                currentPage = 'signup';
            } else {
                currentPage = 'login';
                window.location.hash = '';
            }
        }
    }

    function handleLogout() {
        authStore.logout();
        currentPage = 'login';
        window.location.hash = '';
    }
</script>

<main>
    {#if isInitializing}
        <!-- LOADING SCREEN DURING INITIALIZATION -->
        <div class="loading-screen">
            <div class="spinner"></div>
            <p>Loading...</p>
        </div>
    {:else if !authState.isAuthenticated}
        <!-- UNAUTHENTICATED PAGES -->
        {#if currentPage === 'signup'}
            <Signup />
        {:else}
            <Login />
        {/if}
    {:else}
        <!-- AUTHENTICATED PAGES -->
        {#if currentPage === 'admin' && authState.user?.role === 'admin'}
            <Admin onLogout={handleLogout} />
        {:else if currentPage === 'teacher' && authState.user?.role === 'teacher'}
            <!-- TODO: Create Teacher component -->
            <div class="dashboard">
                <nav class="navbar">
                    <h1>Teacher Dashboard</h1>
                    <div class="nav-right">
                        <span>Welcome, {authState.user?.full_name || 'Teacher'}</span>
                        <span class="role-badge">teacher</span>
                        <button on:click={handleLogout} class="btn-logout">Logout</button>
                    </div>
                </nav>
                <div class="content">
                    <h2>Teacher Dashboard</h2>
                    <p>Welcome to your teacher dashboard! 📚</p>
                </div>
            </div>
        {:else if currentPage === 'student' && authState.user?.role === 'student'}
            <!-- TODO: Create Student component -->
            <div class="dashboard">
                <nav class="navbar">
                    <h1>Student Dashboard</h1>
                    <div class="nav-right">
                        <span>Welcome, {authState.user?.full_name || 'Student'}</span>
                        <span class="role-badge">student</span>
                        <button on:click={handleLogout} class="btn-logout">Logout</button>
                    </div>
                </nav>
                <div class="content">
                    <h2>Student Dashboard</h2>
                    <p>Welcome to your student dashboard! 🎓</p>
                </div>
            </div>
        {:else}
            <!-- DEFAULT DASHBOARD -->
            <div class="dashboard">
                <nav class="navbar">
                    <h1>User Dashboard</h1>
                    <div class="nav-right">
                        <span>Welcome, {authState.user?.full_name || 'User'}</span>
                        <span class="role-badge">{authState.user?.role || ''}</span>
                        <button on:click={handleLogout} class="btn-logout">Logout</button>
                    </div>
                </nav>

                <div class="content">
                    {#if authState.user?.is_approved}
                        <h2>Dashboard - {authState.user.role}</h2>
                        <p>Your account is approved! 🎉</p>
                        <p>Welcome to your personal dashboard.</p>
                    {:else}
                        <div class="pending-approval">
                            <h2>⏳ Pending Approval</h2>
                            <p>Your account is waiting for administrator approval.</p>
                            <p>Please check back later or contact an administrator.</p>
                        </div>
                    {/if}
                </div>
            </div>
        {/if}
    {/if}
</main>

<style>
    :global(body) {
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    main {
        min-height: 100vh;
    }

    /* LOADING SCREEN */
    .loading-screen {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .spinner {
        width: 50px;
        height: 50px;
        border: 5px solid rgba(255, 255, 255, 0.3);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .loading-screen p {
        margin-top: 20px;
        font-size: 1.2rem;
    }

    /* DASHBOARD STYLES */
    .dashboard {
        min-height: 100vh;
        background: #f5f5f5;
    }

    .navbar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .navbar h1 {
        margin: 0;
        font-size: 1.5rem;
    }

    .nav-right {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .role-badge {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        text-transform: capitalize;
    }

    .btn-logout {
        background: white;
        color: #667eea;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        font-weight: 600;
        transition: transform 0.2s;
    }

    .btn-logout:hover {
        transform: translateY(-2px);
    }

    .content {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .pending-approval {
        background: white;
        padding: 3rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .pending-approval h2 {
        color: #ff9800;
        margin-bottom: 1rem;
    }

    .pending-approval p {
        color: #666;
        line-height: 1.6;
    }
</style>
