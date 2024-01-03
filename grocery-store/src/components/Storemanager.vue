<template>
    <div id="navigation_bar">
        <div class="row">
            <div class="col-auto">
                <RouterLink to="/Storemanager"><h1 id="wp_name">
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
            <button v-on:click="getcategories" class="pannelbt pannelbt1"><i class="bi bi-plus-circle" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>Add Product</button>
            <button v-on:click="getproducts" class="pannelbt pannelbt1"><i class="bi bi-dash-circle" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>Edit/Remove Product</button>
            <button v-on:click="addcategory" class="pannelbt pannelbt1"><i class="bi bi-plus-circle" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>Add Category</button>
            <button v-on:click="getmyrequests" class="pannelbt pannelbt1"><i class="bi bi-chat-right-text" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>My Requests</button>
            <hr id="line">
        </div>
        <div class="col-md-8 contentpannel">
            <div v-if="option == 1">
                <label style="margin-left:1.7%; font-size:140% !important;">Product Name</label>
                <input v-model="productname" type="text" placeholder="Enter product name" style="outline: none; margin-left: 1%;margin-right: 1%; height: 40px; width:20%;">
                <label style="margin-left:1.7%; font-size:140% !important;">Category</label>
                <select id="productselect" v-model="pcategoryname" required>
                    <option selected disabled>Select Category</option>
                    <option v-for="c in prcat">{{ c[1] }}</option>
                </select><br><br>
                <label style="margin-left:1.7%; font-size:140% !important;">Mfg date</label>
                <input v-model="mfgdate" type="date" placeholder="Enter product name" style="outline: none; margin-left: 4.5%;margin-right: 1%; height: 40px; width:20%;">
                <label style="margin-left:1.7%; font-size:140% !important;">Exp date</label>
                <input v-model="expdate" type="date" placeholder="Enter product name" style="outline: none; margin-left: 1%;margin-right: 1%; height: 40px; width:20%;"><br><br>
                <label style="margin-left:1.7%; font-size:140% !important;">Description</label>
                <textarea v-model="pdescription" style="margin-left:3%; resize:none;outline:none;" rows="5" cols="94" placeholder="Enter product description"></textarea><br><br>
                <label style="margin-left:1.7%; font-size:140% !important;">Price</label>
                <input v-model="productprice" type="number" step=0.01 min=0 placeholder="Enter product price" style="outline: none; margin-left: 7%;margin-right: 1%; height: 40px; width:20%;">
                <label style="margin-left:1.7%; font-size:140% !important;">Quantity</label>
                <input v-model="productqty" type="number" step=1 min=0 placeholder="Enter quantity" style="outline: none; margin-left: 1%;margin-right: 1%; height: 40px; width:20%;"><br><br>
                <label style="margin-left:1.7%; font-size:140% !important;">Weight</label>
                <input v-model="productweight" type="text" placeholder="Enter weight in g/l/units" style="outline: none; margin-left: 5.7%;margin-right: 1%; height: 40px; width:20%;"><br><br>
                <button v-on:click="addproduct" class="btn" id="decline" style="margin-left:12%;height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Add product</button>
            </div>
            <div v-if="option == 2">
                <table style="margin-left:1.7%;">
                    <th>Product Name</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Weight</th>
                    <tr v-for="p in products" style="font-family:'Lato'; font-size:larger;">
                        <td style="width:18%;">
                            {{ p[1] }}
                        </td>
                        <td style="width:10%;">
                            {{ p[3] }}
                        </td>
                        <td style="width:20%;">
                            {{ p[7] }}
                        </td>
                        <td style="width:10%;">
                            {{ p[8] }}
                        </td>
                        <td style="width:10%;">
                            {{ p[9] }}
                        </td>
                        <td style="width:10%;">
                            {{ p[10] }}
                        </td>
                        <td style="width:15%">
                            <button v-on:click="editproduct(p)" class="btn" style="height:40px;font-family:'Lato';background-color:#FF3269;color:white; margin-right:2%;">Edit</button>
                            <button v-on:click="removeproduct(p[0])" class="btn" style="height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Remove</button>
                        </td>
                    </tr>
                </table>
            </div>
            <div v-if="option == 3">
                <label style="margin-left:1.7%; font-size:140% !important;">Product Name</label>
                <input v-model="productname" type="text" placeholder="Enter product name" style="outline: none; margin-left: 1%;margin-right: 1%; height: 40px; width:20%;">
                <label style="margin-left:1.7%; font-size:140% !important;">Category</label>
                <select id="productselect" v-model="pcategoryname" required>
                    <option selected disabled>Select Category</option>
                    <option v-for="c in prcat">{{ c[1] }}</option>
                </select><br><br>
                <label style="margin-left:1.7%; font-size:140% !important;">Mfg date</label>
                <input v-model="mfgdate" type="date" placeholder="Enter product name" style="outline: none; margin-left: 4.5%;margin-right: 1%; height: 40px; width:20%;" disabled>
                <label style="margin-left:1.7%; font-size:140% !important;">Exp date</label>
                <input v-model="expdate" type="date" placeholder="Enter product name" style="outline: none; margin-left: 1%;margin-right: 1%; height: 40px; width:20%;" disabled><br><br>
                <label style="margin-left:1.7%; font-size:140% !important;">Description</label>
                <textarea v-model="pdescription" style="margin-left:3%; resize:none;outline:none;" rows="5" cols="94" placeholder="Enter product description"></textarea><br><br>
                <label style="margin-left:1.7%; font-size:140% !important;">Price</label>
                <input v-model="productprice" type="number" step=0.01 min=0 placeholder="Enter product price" style="outline: none; margin-left: 7%;margin-right: 1%; height: 40px; width:20%;">
                <label style="margin-left:1.7%; font-size:140% !important;">Quantity</label>
                <input v-model="productqty" type="number" step=1 min=0 placeholder="Enter quantity" style="outline: none; margin-left: 1%;margin-right: 1%; height: 40px; width:20%;"><br><br>
                <label style="margin-left:1.7%; font-size:140% !important;">Weight</label>
                <input v-model="productweight" type="text" placeholder="Enter weight in g/l/units" style="outline: none; margin-left: 5.7%;margin-right: 1%; height: 40px; width:20%;" disabled><br><br>
                <button v-on:click="saveproduct(this.pid)" class="btn" id="decline" style="margin-left:12%;height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Save</button>
                <button v-on:click="cancel" class="btn" id="decline" style="margin-left:2%;height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Cancel</button>
            </div>
            <div v-if="option == 4">
                <label style="margin-left:1.7%;">Category Name</label>
                <input v-model="categoryname" type="text" placeholder="Enter category name" style="outline: none; margin-left: 1%;margin-right: 1%; height: 40px; width:20%;">
                <button v-on:click="sendreq" class="btn" id="decline" style="height:40px;font-family:'Lato';background-color:#FF3269;color:white;">Add category</button>
                <h2 style="margin-left:1.7%;margin-top:4%;">Existing categories</h2>
                <br><p v-if="prcat.length == 0" style="margin-left: 1.7%;">No categories added</p>
                <ul v-else style="list-style-type:disc; margin-left:1.7%">
                <span v-for="cat in prcat">
                    <li style="font-family: 'Lato'; font-size:180%;  margin-top:1%;">{{ cat[1] }}</li>
                </span>
                </ul>
            </div>
            <div v-if="option == 5">
                <div v-if="myrequests.length==0" ><h1 style="font-family:'Lato';margin-left:1.7%;">No requests made</h1></div>
                <div v-else v-for="r in myrequests" class="card card1" style="width: 70%;margin-left:1.7%; margin-bottom:2%;">
                    <div class="card-body">
                        <h2 class="card-title">{{ r[0] }}</h2>
                        <p class="card-text" style="color:black; font-weight:lighter; font-size:larger;">Category name : {{r[2]}}</p>
                        <div v-if="r[3] == 'approved'" style="text-align:center;margin-left:90%; color:#ffffff; background-color:rgb(82, 183, 93); width:fit-content; border-radius: 0.375rem; padding: 0.25rem 0.5rem; font-size: .8rem; font-weight: 600;">{{ r[3]}}</div>
                        <div v-if="r[3] == 'pending'" style="text-align:center;margin-left:90%; color:#ffffff; background-color:rgb(232, 108, 55); width:fit-content; border-radius: 0.375rem; padding: 0.25rem 0.5rem; font-size: .8rem; font-weight: 600;">{{ r[3]}}</div>
                        <div v-if="r[3] == 'declined'" style="text-align:center;margin-left:90%; color:#ffffff; background-color:rgb(239, 79, 95); width:fit-content; border-radius: 0.375rem; padding: 0.25rem 0.5rem; font-size: .8rem; font-weight: 600;">{{ r[3]}}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>

import axios from 'axios';

    export default{
        name : 'Storemanager',

        data(){
            return{
                isLoggedIn : false,
                name : '',
                myrequests : [],
                option : 1,
                prcat : [],
                productname : '',
                pcategoryname : '',
                mfgdate : '',
                expdate : '',
                pdescription : '',
                productprice : 0,
                productqty : 0,
                productweight : '',
                storeid : '',
                products : [],
                pid : '',
                categoryname : '',
                smid : localStorage.getItem('managerid'),
            }
        },

        created(){
            if(localStorage.getItem('token')){
                this.isLoggedIn = true
                this.name = localStorage.getItem('name')
            }
        },

        methods : {
            async getcategories(){
                this.productname = ""
                this.pcategoryname = ""
                this.mfgdate = ""
                this.expdate = ""
                this.pdescription = ""
                this.productprice = ""
                this.productqty = ""
                this.productweight = ""
                this.option = 1
                const cat = await axios.get('/storemanager/addproduct')
                this.prcat = cat.data.categories
            },

            async addproduct(){
                if(this.productname == ""){
                    console.log("entered")
                    alert("Enter product name")
                }
                else if(this.pcategoryname == ""){
                    alert("Select product category")
                }
                else if(this.mfgdate == ""){
                    alert("Select Mfg date")
                }
                else if(this.expdate == ""){
                    alert("Select Exp date")
                }
                else if(this.mfgdate > this.expdate){
                    alert("Enter correct Mfg date and Exp Date")
                }
                const date = new Date()
                let todaydate = date.toJSON().slice(0,10)
                if(todaydate >= this.expdate){
                    alert("The product is already experied")
                }
                else if(this.pdescription == ""){
                    alert("Enter product description")
                }
                else if(this.productprice == ""){
                    alert("Enter price")
                }
                else if(this.productqty == ""){
                    alert("Enter quantity")
                }
                else if(this.productweight == ""){
                    alert("Enter product weight")
                }
                else{
                    const p = await axios.post('/storemanager/addproduct', {
                        pname : this.productname,
                        pcatname : this.pcategoryname,
                        storeid : localStorage.getItem('storeid'),
                        mfg : this.mfgdate,
                        exp : this.expdate,
                        desc : this.pdescription,
                        price : this.productprice,
                        pqty : this.productqty,
                        weight : this.productweight
                    })

                    if(p.data.status == 'unsuccessfull'){
                        alert("Product already exists")
                    }
                    else{
                        alert("Product added successfully")
                        this.productname = ""
                        this.pcategoryname = ""
                        this.mfgdate = ""
                        this.expdate = ""
                        this.pdescription = ""
                        this.productprice = ""
                        this.productqty = ""
                        this.productweight = ""
                    }
                }
            },

            async getproducts(){
                this.option = 2
                const pr = await axios.get('/storemanager/removeproduct')
                this.products  = pr.data.products
            },

            async removeproduct(pid){
                if(confirm("Do you want to remove this product") == true){
                    const pr = await axios.delete('/storemanager/removeproduct', {
                        data : {
                            productid : pid
                        }
                    })
                    if(pr.data.status == 'successfull'){
                        alert("Product deleted successfully")
                    }
                    this.products = pr.data.products
                }
            },

            async editproduct(p){
                this.option = 3
                this.productname = p[1]
                this.pcategoryname = p[3]
                this.mfgdate = p[5]
                this.expdate = p[6]
                this.pdescription = p[7]
                this.productprice = p[8]
                this.productqty = p[9]
                this.productweight = p[10]
                this.pid = p[0]
                const cat = await axios.get('/storemanager/addproduct')
                this.prcat = cat.data.categories
            },

            async cancel(){
                this.option = 2
            },

            async saveproduct(){
                if(confirm("Do you want save the changes") == true){
                    const p = await axios.post('/storemanager/removeproduct', {
                        pid : this.pid,
                        pname : this.productname,
                        pcatname : this.pcategoryname,
                        desc : this.pdescription,
                        price : this.productprice,
                        pqty : this.productqty
                    })
                    alert("Product details updated successfully")
                    this.products = p.data.products
                    this.option = 2
                }
            },

            async addcategory(){
                this.option = 4
            },
            
            async getmyrequests(){
                this.option = 5
                const req = await axios.get('/storemanager/addcategory')
                this.myrequests = req.data.requests
            },

            async sendreq(){
                let x = this.categoryname
                let i
                for(i=0;i<this.prcat.length;i++){
                    if(x==i[1]){
                        alert("Category already exists")
                    }
                }
                this.categoryname = ""
                if(x != "")
                {
                    const cat = await axios.post('/storemanager/addcategory', {
                        catname : x,
                        smid : localStorage.getItem('managerid')
                    })
                    if(cat.data.status == 'successfull'){
                        alert("request sent for approval")
                    }
                }
                else
                {
                    alert("Category name should not be empty")
                }
            }

        },

        mounted() {
            this.getcategories()
        }
    }
</script>

<style>
    @import '../assets/Home.css'
</style>