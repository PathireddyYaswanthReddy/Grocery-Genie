<template>
    <div>
        <h1 class="hed1">
            Grocery Genie
        </h1>
        <div class="cont">
            <h1 style="color:#3c006b; text-align: center; font-family: 'Lato';font-weight:bolder; font-size:3.5rem;">Sign up</h1>
            <div class="inpu">
                <div>
                    <label>User name</label>
                    <input type="text" v-model="username" placeholder="User name" required>   
                </div>
                <br>
                <div>
                    <label>Email</label>
                    <input type="email" v-model="email" placeholder="Email" required>   
                </div>
                <div>
                    <br>
                    <label>Password</label>
                    <input type="password" v-model="password" placeholder="Password" required>
                </div>
                <div>
                    <br>
                    <label>Select Role</label>
                    <br>
                    <select v-model="role" required>
                        <option selected disabled>Select Role</option>
                        <option value="sm">Store Manager</option>
                        <option value="u">User</option>
                    </select>
                </div>
            </div>
            <br>
            <button v-on:click="signup" style="border-radius:30px;outline: none;">Sign up</button>
            <br>
            <p>
                Already have an account? 
            <RouterLink to="/Login">Login</RouterLink>
            </p>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default{
        name: 'SignUp',
        data(){
            return{
                username : '',
                email : '',
                password : '',
                role : ''
            }
        },
        
        methods : {
            async signup(){
                if(this.username == "")
                {
                    alert("Enter username")
                }
                else if(this.email == "")
                {
                    alert("Enter email")
                }
                else if(!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(this.email)))
                {
                    alert("Enter valid email");
                }
                else if(this.password == "")
                {
                    alert("Enter password")
                }
                else if(this.role == "")
                {
                    alert("select role")
                }
                else{
                    let details = await axios.post('signup',{
                        username : this.username,
                        email : this.email,
                        password : this.password,
                        role : this.role
                    });
                    if(details.data.status == "unsuccessfull")
                    {
                        alert("Email id already exists")
                        this.$router.push({name:'Login'})
                    }
                    else if(details.data.status == "successfull")
                    {
                        this.$router.push({name:'Login'})
                    }
                }
            }


        }
    }
</script>

<style>
    @import '../assets/SignUp.css';
</style>