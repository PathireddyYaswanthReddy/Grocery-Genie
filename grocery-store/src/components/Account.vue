<template>
    <div id="navigation_bar">
        <div class="row">
            <div class="col-auto">
                <RouterLink v-if="this.role=='user'" to="/UserHome"><h1 id="wp_name">
                    Grocery Genie
                </h1></RouterLink>
                <RouterLink v-if="this.role=='sm'" to="/Storemanager"><h1 id="wp_name">
                    Grocery Genie
                </h1></RouterLink>
                <RouterLink v-if="this.role=='admin'" to="/Admin"><h1 id="wp_name">
                    Grocery Genie
                </h1></RouterLink>
            </div>
            <div v-if="false" class="col-auto" style="margin-top: -10px;">
            <RouterLink to="/Login"><button id="uname">Login</button></RouterLink>
            </div>
            <div v-if="true" class="col-auto" style="margin-top: -10px;">
                <RouterLink to="/MyAccount"><button id="uname">My Account</button></RouterLink>
            </div>
        </div>
    </div>
    <div class="row" style="margin-right: 0px !important; margin-left: 0px !important;">
        <div class="col-md-2" id="sidepannel">
            <h4 style="color: #ffffff; padding-left:10px;">Hi, {{ name }}</h4>
            <p style="color: #ffffff; padding-left:10px; font-family:'Lato';" v-if="this.role=='sm'">Store Name : {{ this.storename }}&nbsp;&nbsp;&nbsp;<i v-on:click="changename()" style="cursor:pointer;" class="bi bi-pencil"></i></p>
            <hr id="line">
            <button v-if="this.role=='user'" v-on:click="getorders()" class="pannelbt pannelbt1"><i class="bi bi-bag" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>My orders</button>
            <button v-if="this.role=='sm'" v-on:click="this.option = 3" class="pannelbt pannelbt1"><i class="bi bi-box" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>Products Summary</button>
            <button v-if="this.role=='sm'" v-on:click="this.option = 4" class="pannelbt pannelbt1"><i class="bi bi-clipboard-check" style="padding-right: 1.5rem;padding-left: 1.5rem;"></i>Orders Summary</button>
            <hr v-if="this.role!='admin'" id="line">
            <button class="pannelbt pannelbt1" style="text-align: center;" v-on:click="logout">Log out</button>
        </div>
        <div class="col-md-8 contentpannel">
            <div v-if="this.option==1" v-for="i in this.orders" class="card card6">
                <div v-on:click="getorderdetails(i[0],i[5])" class="card-body">
                    <p style="font-weight: bold; font-family:'Lato'; font-size:2rem;">Orderid: {{ i[0] }}</p>
                    <p class="description-ellipsis" style="color:#2B1E35B3; font-family:'Lato';">{{ i[3] }} at {{ i[4] }} </p>
                    <p style="font-weight: bold; font-family:'Lato';font-size:larger;"><span style="color:black;">&#8377;</span>{{ i[5] }}</p>
                </div>
            </div>
            <div v-if="this.option==2" class="card card7">
                <div v-for="i in this.orderdetails">
                <div class="card-body">
                    <p style="font-weight: bold; font-family:'Lato'; font-size:2rem;">{{ i[2] }}</p>
                    <p class="description-ellipsis" style="color:#2B1E35B3; font-family:'Lato';">Qty: {{ i[3] }}</p>
                    <p class="description-ellipsis" style="color:#2B1E35B3; font-family:'Lato';">Price: <span style="color:#2B1E35B3;">&#8377;</span>{{ i[4]*i[3] }}</p>
                    <hr>
                </div></div>
                <table style="margin-left:1.7%">
                    <tr>
                        <td style="width:85%;"><h4>Total</h4></td>
                        <td><h4><span style="color:black;">&#8377;</span>{{ this.totalprice }}</h4></td>
                    </tr>
                </table>
            </div>
            <div v-if="this.option == 3">
                <p style="font-family:'Lato'; font-size:larger;"><strong><a v-on:click="productreport()" style="cursor: pointer;">Click here</a></strong> to download the product summary report.</p>
            </div>
            <div v-if="this.option == 4">
                <p style="font-family:'Lato'; font-size:larger;"><strong><a v-on:click="orderreport()" style="cursor: pointer;">Click here</a></strong> to download the orders summary report.</p>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios'

    export default{
        name : 'Account',

        data(){
            return{
                role : '',
                name : '',
                orders : [],
                orderdetails : [],
                option : 1,
                totalprice : 0,
                isWaiting: false,
                storename : ''
            }
        },

        created(){
            if(localStorage.getItem('token')){
                this.role = localStorage.getItem('role')
                this.name = localStorage.getItem('name')
                if(this.role=='sm'){
                    this.storename = localStorage.getItem('storename')
                }
            }
        },

        methods : {
            async logout(){
                localStorage.removeItem('token')
                if(localStorage.getItem('role') == 'sm'){
                    localStorage.removeItem('storeid')
                    localStorage.removeItem('storename')
                    localStorage.removeItem('managerid')
                }
                localStorage.removeItem('role')
                localStorage.removeItem('name')
                this.$router.push({name:'Login'})
            },

            async getorders(){
                this.option = 1
                const orddetails = await axios.get('/myaccount/' + localStorage.getItem('email'))
                this.orders = orddetails.data.orders
                this.totalprice = 0
            },

            async getorderdetails(ordid,totalprice){
                this.option = 2
                const details = await axios.get('/myaccount/' + localStorage.getItem('email')+ '/' + ordid)
                this.orderdetails = details.data.orderdetails
                this.totalprice = totalprice
            },

            async productreport(){
                const details = await axios.get('/productsreport/' + localStorage.getItem('storeid'))
                const taskid = details.data.taskid
                this.isWaiting = true
                while(this.isWaiting == true){
                    const statusresponse = await axios.get('/productsreportstatus/' + taskid)
                    if(statusresponse.status){
                        this.isWaiting = false
                    }
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }

                if(this.isWaiting == false){
                        const downloadResponse = await axios.get(`/productsreportstatus/${taskid}`, {
                        responseType: 'blob',
                    });

                    const blob = new Blob([downloadResponse.data], { type: downloadResponse.headers['content-type'] });
                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = 'productssummary.csv';
                    link.click();
                    window.URL.revokeObjectURL(link.href);

                    alert('Report downloaded successfully');
                }
            },

            async orderreport(){
                const details = await axios.get('/ordersreport/' + localStorage.getItem('storeid'))
                const taskid = details.data.taskid
                this.isWaiting = true
                while(this.isWaiting == true){
                    const statusresponse = await axios.get('/orderreportstatus/' + taskid)
                    if(statusresponse.status){
                        this.isWaiting = false
                    }
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }

                if(this.isWaiting == false){
                        const downloadResponse = await axios.get(`/orderreportstatus/${taskid}`, {
                        responseType: 'blob',
                    });

                    const blob = new Blob([downloadResponse.data], { type: downloadResponse.headers['content-type'] });
                    const link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = 'orderssummary.csv';
                    link.click();
                    window.URL.revokeObjectURL(link.href);

                    alert('Report downloaded successfully');
                }
            },

            async changename(){
                var stname = prompt("Enter New Store Name")
                if(stname != null){
                    const n = await axios.post(`/storemanager/changestorename/${localStorage.getItem('storeid')}` , {
                        newname : stname
                    })
                    localStorage.setItem('storename' , stname)
                    this.storename = stname
                }
            }

        },

        mounted() {
            if(this.role == 'user')
            {
                this.getorders()
            }
            else if(this.role=='sm'){
                this.option = 3
            }
            
        }

    }
</script>

<style>
    @import '../assets/Home.css'
</style>