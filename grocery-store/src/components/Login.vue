<template>
    <div>
        <h1 class="hed1">
            Grocery Genie
        </h1>
        <div v-if="l==2" class="alert alert-info alert-dismissible fade show" style="width:50%; margin-left:25%; margin-top:4%; text-align:center;" role="alert">
            Please choose the role you'd like to log in for.
            <span style="margin-right: 20px; margin-left:5px;"><RouterLink v-on:click="assignuser" to="/UserHome">User</RouterLink></span><span><RouterLink v-on:click="assignsm" to="/Storemanager">Store Manager</RouterLink></span>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="cont">
            <h1 style="color:#3c006b; text-align: center; font-family: 'Lato'; font-weight:bolder; font-size:3.5rem;">Login</h1>
            <div class="inpu">
                <div>
                    <label>Email</label>
                    <input type="text" v-model="email" placeholder="Email" required>   
                </div>
                <div>
                    <br>
                    <label>Password</label>
                    <input type="password" v-model="password" placeholder="Password" required>
                </div>
            </div>
            <br>
            <button v-on:click="login" style="border-radius:30px;outline: none;">Login</button>
            <br>
            <p>
                Don't have an account? 
            <RouterLink to="/SignUp">Sign up</RouterLink>
            </p>
        </div>
    </div>
</template>
    
<script>
    import axios from 'axios';

    export default{
        name: 'Login',
        data(){
            return{
                email : '',
                password : '',
                l : 1,
                names : []
            }
        },
        
        methods : {
            async login(){
                if(this.email == "")
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
                else{
                    let details = await axios.post('/login',{
                        email : this.email,
                        password : this.password,
                    });
                    if(details.data.status == "incorrect")
                    {
                        alert("Incorrect username or password")
                    }
                    else if(details.data.status == "unsuccessfull")
                    {
                        alert("User doesn't exist")
                        this.$router.push({name:'SignUp'})
                    }
                    else if(details.data.status == "pending")
                    {
                        alert("Request not yet approved by admin")
                    }
                    else if(details.data.status == "declined")
                    {
                        alert("Request declined by admin")
                    }
                    else if(details.data.status == "successfull")
                    {
                        localStorage.setItem('token', details.data.token)
                        const r = details.data.role
                        this.names = details.data.name
                        if(r.length == 1)
                        {
                            if(r[0] == 'user')
                            {   
                                localStorage.setItem('role',r[0])
                                localStorage.setItem('name',this.names[0])
                                localStorage.setItem('email', details.data.email)
                                this.$router.push({name:'UserHome'})
                            }
                            else if(r[0] == 'sm')
                            {
                                localStorage.setItem('role',r[0])
                                localStorage.setItem('name',this.names[0])
                                localStorage.setItem('storeid' , details.data.storeid)
                                localStorage.setItem('storename' , details.data.storename)
                                localStorage.setItem('managerid' , details.data.managerid)
                                localStorage.setItem('email', details.data.email)
                                this.$router.push({name:'Storemanager'})
                            }
                            else if(r[0] == 'admin')
                            {
                                localStorage.setItem('role',r[0])
                                localStorage.setItem('name',this.names[0])
                                localStorage.setItem('email', details.data.email)
                                this.$router.push({name:'Admin'})
                            }
                        }
                        else
                        {
                            this.l = 2
                        }
                    }
                }
            },

            async assignuser(){
                localStorage.setItem('role','user')
                localStorage.setItem('name',this.names[0])
                localStorage.setItem('email', details.data.email)
            },

            async assignsm(){
                localStorage.setItem('role','sm')
                localStorage.setItem('name',this.names[1])
                localStorage.setItem('storeid' , details.data.storeid)
                localStorage.setItem('storename' , details.data.storename)
                localStorage.setItem('managerid' , details.data.managerid)
                localStorage.setItem('email', details.data.email)
            }
        }
    }
</script>
    
    
<style>
    @import '../assets/SignUp.css';
</style>