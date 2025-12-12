<script>
    import { api } from './api';

    let formData = {
        email: '',
        full_name: '',
        password: '',
        confirmPassword: '',
        role: ''
    };
    
    let error = '';
    let success = false;
    let loading = false;

    async function handleSignup() {
        error = '';
        
        if (formData.password !== formData.confirmPassword) {
            error = 'Passwords do not match';
            return;
        }

        loading = true;

        try {
            const { confirmPassword, ...userData } = formData;
            await api.signup(userData);
            success = true;
        } catch (err) {
            error = err.message;
        } finally {
            loading = false;
        }
    }
</script>

<div class="auth-container">
    <div class="auth-card">
        <h2>Sign Up</h2>
        
        {#if success}
            <div class="success-message">
                <p>Registration successful!</p>
                <p>Your account is pending approval from an administrator.</p>
                <button on:click={() => window.location.hash = '#/login'} class="btn-primary">
                    Go to Login
                </button>
            </div>
        {:else}
            {#if error}
                <div class="error-message">{error}</div>
            {/if}

            <form on:submit|preventDefault={handleSignup}>
                

                <div class="form-group">
                    <label for="email">Email</label>
                    <input 
                        id="email"
                        type="email" 
                        bind:value={formData.email}
                        placeholder="your.email@example.com"
                        required
                        disabled={loading}
                    />
                </div>

                <div class="form-group">
                    <label for="full_name">Full Name</label>
                    <input 
                        id="full_name"
                        type="text" 
                        bind:value={formData.full_name}
                        placeholder="Your full name"
                        required
                        disabled={loading}
                    />
                </div>

                <div class="form-group">
                    <label for="role">Role</label>
                    <select id="role" bind:value={formData.role} disabled={loading}>
                        <option value="student">Student</option>
                        <option value="teacher">Teacher</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input 
                        id="password"
                        type="password" 
                        bind:value={formData.password}
                        placeholder="Enter password"
                        required
                        disabled={loading}
                    />
                </div>

                <div class="form-group">
                    <label for="confirmPassword">Confirm Password</label>
                    <input 
                        id="confirmPassword"
                        type="password" 
                        bind:value={formData.confirmPassword}
                        placeholder="Confirm password"
                        required
                        disabled={loading}
                    />
                </div>

                <button type="submit" class="btn-primary" disabled={loading}>
                    {loading ? 'Creating account...' : 'Sign Up'}
                </button>
            </form>

            <p class="auth-link">
                Already have an account? <button on:click={() => window.location.hash = '#/login'}>Login</button>
            </p>
        {/if}
    </div>
</div>

<style>
    .auth-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
    }

    .auth-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 400px;
    }

    h2 {
        text-align: center;
        color: #333;
        margin-bottom: 1.5rem;
    }

    .form-group {
        margin-bottom: 1rem;
    }

    label {
        display: block;
        margin-bottom: 0.5rem;
        color: #555;
        font-weight: 500;
    }

    input, select {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 5px;
        font-size: 1rem;
        transition: border-color 0.3s;
    }

    input:focus, select:focus {
        outline: none;
        border-color: #667eea;
    }

    input:disabled, select:disabled {
        background-color: #f5f5f5;
        cursor: not-allowed;
    }

    .btn-primary {
        width: 100%;
        padding: 0.75rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s;
        margin-top: 0.5rem;
    }

    .btn-primary:hover:not(:disabled) {
        transform: translateY(-2px);
    }

    .btn-primary:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }

    .error-message {
        background: #fee;
        color: #c33;
        padding: 0.75rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        text-align: center;
    }

    .success-message {
        text-align: center;
        padding: 1rem;
    }

    .success-message p {
        color: #28a745;
        margin-bottom: 1rem;
    }

    .auth-link {
        text-align: center;
        margin-top: 1rem;
        color: #666;
    }

    .auth-link button {
        background: none;
        border: none;
        color: #667eea;
        cursor: pointer;
        font-weight: 600;
        text-decoration: underline;
    }
</style>
