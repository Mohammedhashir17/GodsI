const mongoose=require('mongoose');
const mongoURI="mongodb+srv://admin:admin@cluster0.dfeat.mongodb.net/"

const connectToMongo=()=>{
    mongoose.connect(mongoURI,()=>{
        console.log("connected to mongo successfully");
    })
}
module.exports=connectToMongo;