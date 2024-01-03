<template>
    <div id="navigation_bar">
        <div class="row">
            <div class="col-auto">
                <h1 v-on:click="changeoption" id="wp_name">
                    Grocery Genie
                </h1>
            </div>
            <div class="col-auto">
                <select v-model="selectedstore" id="store_selector">
                    <option selected disabled>Select Store</option>
                    <option v-for="st in stores" v-bind:value="st[0]">{{ st[1] }}</option>
                </select>
            </div>
            <div class="col-auto">
                <input v-if="this.option == 1" v-on:click="checkstore()" v-model="searchCategory" type="text" name="search" id="search" placeholder="🔍 Search over 5000 products">
            </div>
            <div class="col-auto">
                <input v-if="this.option == 2" v-on:click="checkstore()" v-model="searchProduct" type="text" name="search" id="search" placeholder="🔍 Search over 5000 products">
            </div>
            <div v-if="!(isLoggedIn)" class="col-auto" style="margin-top: -10px;">
            <RouterLink to="/Login"><button id="uname">Login</button></RouterLink>
            </div>
            <div v-if="isLoggedIn" class="col-auto" style="margin-top: -10px;">
                <RouterLink to="/MyAccount"><button id="uname">My Account</button></RouterLink>
            </div>
            <div v-if="Object.keys(this.cart).length == 0" class="col-auto">
                <button v-on:click="mycart()" style="font-family:'Lato';background-color:#FF3269; border: none;outline: none; color: #ffffff; margin-top: 10px;font-size: 1.25rem;height: 3.5rem;
                width: 10rem;
                justify-content: center;
                border-radius: 0.5rem;
                margin-top:-0.25rem;"><i class="bi bi-bag" style="padding-right: 0.75rem;"></i>My cart</button>
            </div>
            <div v-else class="col-auto">
                <button v-on:click="mycart()" style="font-family:'Lato';background-color:#FF3269; border: none;outline: none; color: #ffffff; margin-top: 10px;font-size: 1.25rem;height: 3.5rem;
                width: 10rem;
                justify-content: center;
                border-radius: 0.5rem;
                margin-top:-0.25rem;"><i class="bi bi-bag" style="padding-right: 0.75rem;"></i>{{ this.items }} items
                <span style="color:white; display:block;width:fit-content;padding-left: 3.75rem;"><span style="color:white;">&#8377;</span>{{ this.totalprice }}</span></button>
            </div>
        </div>
    </div>
    <div v-on:click="checkstore()" class="row" style="margin-top: 5%; margin-right: 0px !important; margin-left: 0px !important;" >
        <div v-if="this.option == 1 || this.option == 2" class="col-md-1">
        </div>
        <div v-if="this.option == 1" class="col-md-10">
            <br>
            <p style="font-family:'Lato';font-weight: 700;font-size: 1.5rem;letter-spacing: 1px; font-weight:bold;">Explore By Categories</p>
            <div v-if="this.searchCategory == ''" class="row row-cols-1 row-cols-md-3 g-4">
                <div v-for="c in categories" class="card">
                    <h2 v-on:click="getcatproducts(c[0],c[1])" class="card-title" style="color: #45155b; font-weight:bolder;">{{ c[1] }}</h2>
                </div>
            </div>
            <div v-else class="row row-cols-1 row-cols-md-3 g-4">
                <div v-if="filteredCategories.length == 0"> There are no categories matching that name</div>
                <div v-else v-for="c in filteredCategories" class="card">
                    <h2 v-on:click="getcatproducts(c[0],c[1])" class="card-title" style="color: #45155b; font-weight:bolder;">{{ c[1] }}</h2>
                </div>
            </div>
        </div>
        <div v-if="this.option == 2" class="col-md-2">
            <div class="categoryselector">
                <div class="card card3" v-for="c in categories" style="width:100%; height:8%;justify-content:center;align-text:center;background-color:white;border-radius:0rem;pointer:;">
                   <h4 v-on:click="getcatproducts(c[0],c[1])" style="color: #45155b; font-family:'lato';align-content:center;font-weight:bold;">{{ c[1] }}</h4>
                </div>
            </div>
        </div>
        <div v-if="this.option == 2" class="col-md-8" style="margin-top:1%;">
            <h1 style="font-family:'Lato';font-weight:bold;">{{ this.selectedcatname }}</h1>
            <div class="row row-cols-1 row-cols-md-3 g-4">
                <div v-if="filteredProducts.length == 0"> No products available under this category</div>
                <div v-else v-if="this.searchProduct == ''" v-for="p in filteredProducts" class="card card4">
                    <p style="font-weight: bold; font-family:'Lato'; font-size:2rem;">{{ p[1] }}</p>
                    <p class="description-ellipsis" style="color:#2B1E35B3; font-family:'Lato';">{{ p[7] }}</p>
                    <p style="color:#2B1E35B3; font-family:'Lato';">{{ p[10] }}</p>
                    <p style="font-weight: bold; font-family:'Lato';"><span style="color:black;">&#8377;</span>{{ p[8] }}</p>
                    <button v-if="p[9] != 0 && !(this.cart[p[0]])" v-on:click="addproduct(p)" class="btn" id="addbutton">Add</button>
                    <span v-if="this.cart[p[0]] && p[9] != 0" style="display:flex;">
                        <button v-on:click="removeproduct(p)" class="productcount" style="border-top-left-radius: 0.25rem;border-bottom-left-radius: 0.25rem;">-</button>
                        <button class="productcount">{{ cart[p[0]].qty }}</button>
                        <button v-on:click="addproduct(p)" class="productcount" style="border-top-right-radius: 0.25rem;border-bottom-right-radius: 0.25rem;">+</button>
                    </span>
                    <button v-if="p[9] == 0" class="btn" id="addbutton" style="cursor:not-allowed;width:fit-content;">out of stock</button>
                </div>
                <div v-if="filteredSearchProducts.length == 0">No products available under this category with that name</div>
                <div v-else v-if="this.searchProduct != ''" v-for="p in filteredSearchProducts" class="card card4">
                    <p style="font-weight: bold; font-family:'Lato'; font-size:2rem;">{{ p[1] }}</p>
                    <p class="description-ellipsis" style="color:#2B1E35B3; font-family:'Lato';">{{ p[7] }}</p>
                    <p style="color:#2B1E35B3; font-family:'Lato';">{{ p[10] }}</p>
                    <p style="font-weight: bold; font-family:'Lato';"><span style="color:black;">&#8377;</span>{{ p[8] }}</p>
                    <button v-if="p[9] != 0 && !(this.cart[p[0]])" v-on:click="addproduct(p)" class="btn" id="addbutton">Add</button>
                    <span v-if="this.cart[p[0]] && p[9] != 0" style="display:flex;">
                        <button v-on:click="removeproduct(p)" class="productcount" style="border-top-left-radius: 0.25rem;border-bottom-left-radius: 0.25rem;">-</button>
                        <button class="productcount">{{ cart[p[0]].qty }}</button>
                        <button v-on:click="addproduct(p)" class="productcount" style="border-top-right-radius: 0.25rem;border-bottom-right-radius: 0.25rem;">+</button>
                    </span>
                    <button v-if="p[9] == 0" class="btn" id="addbutton" style="cursor:not-allowed;width:fit-content;">out of stock</button>
                </div>
            </div>
        </div>
        <div v-if="this.option == 1 || this.option == 2" v-on:click="checkstore()" class="col-md-1">
        </div>
    </div>
    <div v-if="this.option==3" class="row" style="margin-right: 0px !important; margin-left: 0px !important;" >
        <div class="col-md-2">
        </div>
        <div v-if="Object.keys(this.cart).length > 0" class="col-md-5">
            <div v-for="i in cart" class="card card5">
                <div class="card-body">
                    <p style="font-weight: bold; font-family:'Lato'; font-size:2rem;">{{ i.details[1] }}</p>
                    <p class="description-ellipsis" style="color:#2B1E35B3; font-family:'Lato';">{{ i.details[7] }}</p>
                    <p style="color:#2B1E35B3; font-family:'Lato';">{{ i.details[10] }}</p>
                    <p style="font-weight: bold; font-family:'Lato';"><span style="color:black;">&#8377;</span>{{ i.details[8] }}</p>
                    <span style="display:flex;">
                        <button v-on:click="removeproduct(i.details)" class="productcount" style="border-top-left-radius: 0.25rem;border-bottom-left-radius: 0.25rem;">-</button>
                        <button class="productcount">{{ i.qty }}</button>
                        <button v-on:click="addproduct(i.details)" class="productcount" style="border-top-right-radius: 0.25rem;border-bottom-right-radius: 0.25rem;">+</button>
                    </span>
                </div>
            </div>
        </div>
        <div v-if="Object.keys(this.cart).length > 0" class="col-md-3" style="border-color: black;margin-top:2%;">
            <button v-on:click="emptycart()" style="font-family:'Lato';background-color:white; border-color: none; outline: none; color: #FF3269;font-size: 1.25rem;
                margin-bottom:5%;">Empty cart</button>
            <table>
                <tr>
                    <td style="width:85%;"><h4>Item Total</h4></td>
                    <td><h4><span style="color:black;">&#8377;</span>{{ this.totalprice }}</h4></td>
                </tr>
                <tr style="color:#2B1E35B3; font-family:'Lato';">
                    <td><p>No of items</p></td>
                    <td><p>{{ this.items }}</p></td>
                </tr>
                <hr style="width:120%;">
                <tr>
                    <td style="width:85%;"><h4>To Pay</h4></td>
                    <td><h4><span style="color:black;">&#8377;</span>{{ this.totalprice }}</h4></td>
                </tr>
            </table>
            <button v-on:click="placeorder()" style="font-family:'Lato';background-color:#FF3269; border: none;outline: none; color: #ffffff;font-size: 1.25rem;height: 3rem;
                width: 100%;
                justify-content: center;
                border-radius: 0.5rem;
                margin-top:10%;">Place order</button>
        </div>
        <div v-else class="col-md-8">
            <center>
                <h4>your cart is empty</h4>
                <button v-on:click="this.option=1" class="btn" id="approve" style="font-family:'Lato';border-color:black; color:#FF3269 !important; margin-right:2%;">Browse Products</button>
            </center>
        </div>
        <div class="col-md-2">
        </div>
    </div>
</template>

<script>
import axios from 'axios';

    export default{
    name: 'UserHome',


    data() {
        return {
            isLoggedIn: false,
            categories: [],
            stores: [],
            selectedstore: '',
            option: 1,
            products: [],
            selectedcatid: '',
            selectedcatname: '',
            name: '',
            cart: {},
            items: 0,
            totalprice: 0,
            searchCategory: '',
            searchProduct: ''
        };
    },

    created() {
        if (localStorage.getItem('token')) {
            this.isLoggedIn = true;
            this.name = localStorage.getItem('name');
        }
    },
    methods: {
        async getcategories() {
            const cat = await axios.get('/admin/addcategory');
            this.categories = cat.data.categories;
            const p = await axios.get('user/getproducts');
            this.products = p.data.products;
        },
        async getstores() {
            this.option = 1;
            const st = await axios.get('/user/getstores');
            this.stores = st.data.stores;
        },
        checkstore() {
            if (this.selectedstore == "") {
                alert("Select Store");
            }
        },
        async getcatproducts(catid, catname) {
            if (this.selectedstore != "") {
                this.option = 2;
                this.selectedcatid = catid;
                this.selectedcatname = catname;
            }
        },
        changeoption() {
            this.option = 1;
        },
        addproduct(product) {
            if (this.cart[product[0]]) {
                if(this.cart[product[0]].qty + 1 <= this.cart[product[0]].details[9]){
                    this.cart[product[0]].qty++;
                }
                else{
                    alert("only " + this.cart[product[0]].details[9] + " qty can be ordered")
                }
            }
            else {
                this.cart[product[0]] = {
                        qty: 1,
                        details: product
                    };
            }
            this.items++;
            this.totalprice += Number(product[8]);
        },
        removeproduct(product) {
            if (this.cart[product[0]].qty > 0) {
                this.cart[product[0]].qty--;
                this.items--;
                this.totalprice -= Number(product[8]);
            }
            if (this.cart[product[0]].qty == 0) {
                delete this.cart[product[0]];
            }
        },

        mycart(){
            this.option = 3
        },

        emptycart(){
            this.cart = {}
            this.items = 0
            this.totalprice = 0
        },

        async placeorder(){
            if(confirm("Do you want to place this order") == true){
                var order = await axios.post('/user/orders', {
                    cart : this.cart,
                    storeid : this.selectedstore,
                    email : localStorage.getItem('email'),
                    totalprice : this.totalprice
                })
            }

            if(order.data.status == "successfull"){
                alert("Order placed successfully")
                this.cart = {}
                this.option = 1
                this.items = 0
                this.totalprice = 0
            }
        }
    },
    mounted() {
        this.getcategories();
        this.getstores();
    },
    computed: {
        filteredProducts() {
            return this.products.filter(product => {
                return (product[4] === this.selectedstore &&
                    product[2] === this.selectedcatid);
            });
        },

        filteredCategories(){
            return this.categories.filter(category => {
                return category[1].toLowerCase().includes(this.searchCategory.toLowerCase());
            });
        },

        filteredSearchProducts(){
            const filteredByCategory = this.products.filter(product => {
            return (
                    product[4] === this.selectedstore &&
                    product[2] === this.selectedcatid
                );
            });

            return this.searchProduct
                ? filteredByCategory.filter(product =>
                    product[1].toLowerCase().includes(this.searchProduct.toLowerCase())
                )
                : filteredByCategory;
        }
    },
}
</script>


<style>
    @import '../assets/Home.css'
</style>