<script>
    import { onMount } from 'svelte';
    import { api } from './api.js';
    import { authStore } from '../stores/auth.js'; // Import your auth store
    import UserManagement from './UserManagement.svelte';

    export let onLogout = () => {};

    let user = null;
    let loading = true;

    console.log('🔵 Admin.svelte script executed');

    onMount(async () => {
        console.log('🟢 Admin.svelte onMount called');
        try {
            user = await api.getMe();
            console.log('👤 Admin user fetched:', user);
            loading = false;
        } catch (error) {
            console.error('❌ Auth failed in Admin:', error);
            onLogout();
        }
    });
</script>

{#if loading}
    <div class="loading">Loading...</div>
{:else}
    <div class="admin-container">
        <header>
            <h1>Admin Dashboard</h1>
            <div class="user-info">
                <span>Welcome, {user.full_name}</span>
                <button on:click={onLogout} class="logout-btn">Logout</button>
            </div>
        </header>

        {#key user}
            <UserManagement />
        {/key}
    </div>
{/if}

<style>
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        font-size: 1.5rem;
    }

    .admin-container {
        min-height: 100vh;
        background: #f5f7fa;
    }

    header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    h1 {
        margin: 0;
        font-size: 1.8rem;
    }

    .user-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .logout-btn {
        background: rgba(255,255,255,0.2);
        color: white;
        border: 1px solid white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }

    .logout-btn:hover {
        background: white;
        color: #667eea;
    }
</style>
