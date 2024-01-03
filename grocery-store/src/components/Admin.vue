<template>
    <div id="navigation_bar">
        <div class="row">
            <div class="col-auto">
                <RouterLink to="/Admin"><h1 id="wp_name">
                    Grocery Genie
                </h1></RouterLink>
            </div>
            <div v-if="!(isLoggedIn)" class="col-auto" style="margin-top: -10px;">
            <RouterLink to="/Login"><button id="uname">Login</button></RouterLink>
            </div>
            <div v-if="isLoggedIn" class="col-auto" style="margin-top: -10px;">
                <RouterLink to="/MyAccount"><button id="uname">My Account</button></RouterLink>
            </div>
        </div>
    </div>
    <div class="row" style="margin-right: 0px !important; margin-left: 0px !important;">
        <div class="col-md-2" id="sidepannel">
            <h4 style="color: #ffffff; padding-left:10px;">Hi, {{ name }}</h4>
            <hr id="line">
            <button v-on:click="getpendingreq" class="pannelbt pannelbt1"><i class="bi bi-clock" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>Pending requests</button>
            <button v-on:click="getcategories" class="pannelbt pannelbt1"><i class="bi bi-plus-circle" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>Add/Remove Category</button>
            <hr id="line">
        </div>
        <div class="col-md-8 contentpannel">
            <span v-if="option == 1">
            <div v-if="prequests.length==0" ><h1 style="font-family:'Lato';margin-left:1.7%;">No pending requests</h1></div>
            <div v-else v-for="r in prequests" class="card card1" style="width: 70%;margin-left:1.7%; margin-bottom:2%;">
                <div v-if="r[1] == 'Sign Up request'" class="card-body">
                  <h2 class="card-title">{{ r[1] }}</h2>
                  <p class="card-text">Username : {{r[2]}}</p>
                  <p class="card-text">Email-id : {{r[3]}} </p>
                  <p class="card-text">Store-manager Id : {{r[4]}}</p>
                  <button v-on:click="approve(r[4],'s','')" class="btn" id="approve" style="font-family:'Lato';border-color:black; color:#FF3269 !important; margin-right:2%;">Approve</button>
                  <button v-on:click="decline(r[4],'s','')" class="btn" id="decline" style="font-family:'Lato';border-color:black;">Decline</button>
                </div>
                <div v-else class="card-body">
                    <h2 class="card-title">{{ r[1] }}</h2>
                    <p class="card-text">Store-manager Id : {{r[4]}}</p>
                    <p class="card-text">Category name : {{r[5]}}</p>
                    <button v-on:click="approve(r[4],'c',r[5])" class="btn" id="approve" style="font-family:'Lato';border-color:black; color:#FF3269 !important; margin-right:2%;">Approve</button>
                    <button v-on:click="decline(r[4],'c',r[5])" class="btn" id="decline" style="font-family:'Lato';border-color:black;">Decline</button>
                </div>
            </div></span>
            <div v-if="option == 2">
                <label style="margin-left:1.7%;">Category Name</label>
                <input v-model="categoryname" type="text" placeholder="Enter category name" style="outline: none; margin-left: 1%;margin-right: 1%; height: 40px; width:20%;">
                <button v-on:click="addcat" class="btn" id="decline" style="height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Add category</button>
                <h2 style="margin-left:1.7%;margin-top:4%;">Existing categories</h2>
                <br><p v-if="excategories.length == 0" style="margin-left: 1.7%;">No categories added</p>
                <ul v-else style="list-style-type:disc; margin-left:1.7%">
                <span v-for="cat in excategories">
                    <table>
                        <tr v-if="editid !== cat[0]"><td style="width:70%"><li style="font-family: 'Lato'; font-size:180%;  margin-top:1%;">{{ cat[1] }}</li></td>
                        <td style="width:15%"><button v-on:click="editcat(cat[0],cat[1])" class="btn" id="decline" style="width:60%;height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Edit</button></td>
                        <td><button v-on:click="removecat(cat[0])" class="btn" id="decline" style="height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Remove category</button></td></tr>
                        <tr v-if="editid == cat[0]">
                        <td style="width:85%"><input v-if="editid == cat[0]" v-model="editedname" type="text" style="outline: none;height: 40px; width:80%;"></td>
                        <td><button v-if="editid == cat[0]" v-on:click="savecat(cat[0])" class="btn" id="decline" style="height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Save</button></td>
                        </tr>
                    </table>
                </span>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

    export default{
        name : 'Admin',

        data(){
            return{
                isLoggedIn : false,
                prequests : [],
                name : '',
                managerid : '',
                status : '',
                excategories : [],
                catid : '',
                catname : '',
                editid : null,
                addstatus : '',
                option : 1,
                categoryname : ''
            }
        },
        created(){
            if(localStorage.getItem('token')){
                this.isLoggedIn = true
                this.name = localStorage.getItem('name')
            }
        },

        methods : {
            async getpendingreq(){
                this.option = 1
                const details = await axios.get('/admin/pendingrequests')
                this.prequests = details.data.req
            },

            async approve(managerid,type,catname){
                const details = await axios.post('/admin/pendingrequests', {
                    managerid : managerid,
                    status : 'approved',
                    type : type,
                    catname : catname
                })
                this.prequests = details.data.req
            },

            async decline(managerid,type,catname){
                const details = await axios.post('/admin/pendingrequests', {
                    managerid : managerid,
                    status : 'declined',
                    type : type,
                    catname : catname
                })
                this.prequests = details.data.req   
            },

            async getcategories(){
                this.option = 2
                const cat = await axios.get('/admin/addcategory')
                this.excategories = cat.data.categories
            },

            async removecat(cid){
                if(confirm("Do to want to delete this category?") == true)
                {
                    const cat = await axios.delete('/admin/addcategory', {
                        data : {
                            catid : cid
                        }
                    })
                    this.excategories = cat.data.categories
                }
            },

            async addcat(){
                let x = this.categoryname
                this.categoryname = ""
                if(x != "")
                {
                    const cat = await axios.post('/admin/addcategory', {
                        catname : x,
                        addstatus : 'add'
                    })
                    if (cat.data.status == 'unsuccessfull'){
                        alert("Category already exists")
                    }
                    else{
                        this.excategories = cat.data.categories
                    }
                }
                else
                {
                    alert("Category name should not be empty")
                }
            },

            async editcat(cid,cname){
                if(confirm("Do to want to edit this category?") == true)
                {
                    this.editid = cid
                    this.editedname = cname
                }
            },

            async savecat(cid){
                const cat = await axios.post('/admin/addcategory',{
                    addstatus : 'update',
                    catid : cid,
                    catname : this.editedname
                })
                if(cat.data.status == "unsuccessfull"){
                    alert("Category already exists")
                }
                else{
                    this.editid = null
                    this.excategories = cat.data.categories
                }
            }
        },

        mounted() {
            this.getpendingreq()
        }
    }
</script>

<style>
    @import '../assets/Home.css'
</style>