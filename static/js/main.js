const createOrder = (id)=>{
    try {
        axios.post('api/order',{'id':id}).then(res=>{
            if (res.data.status) {
                window.location='http://127.0.0.1:8000/'
            } 
        })
    } catch (error) {
        window.location='http://127.0.0.1:8000/' 
    }
}