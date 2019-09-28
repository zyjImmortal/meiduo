let vm = new Vue({
    el: '#app',
    data: {
        host: host,
        error_name: false,
        error_password: false,
        error_check_password: false,
        error_phone: false,
        error_allow: false,
        error_image_code: false,
        error_sms_code: false,

        username: '',
        password: '',
        password2: '',
        mobile: '',
        image_code: '',
        sms_code: '',
        sms_code_tip: "获取短信验证码",
        allow: false,
        image_code_id: '',
        image_code_url: '',
        send_flag: false,
        error_image_code_message: '',
        error_sms_code_message: '',
        error_username_message: '',
        error_phone_message: ''
    },
    mounted: function () {
        this.generate_image_code()
        // axios.get("http://127.0.0.1:8000/image_code/" + this.image_code_id).then(response => {
        //
        // })
        //     .catch(error =>{
        //
        //     })
    },
    methods: {
        generate_image_code: function () {
            this.image_code_id = this.generate_uuid();
            this.image_code_url = this.host + "/image_code/" + this.image_code_id;
        },
        // 生成uuid
        generate_uuid: function () {
            var d = new Date().getTime();
            if (window.performance && typeof window.performance.now === "function") {
                d += performance.now(); //use high-precision timer if available
            }
            var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                var r = (d + Math.random() * 16) % 16 | 0;
                d = Math.floor(d / 16);
                return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
            });
            return uuid;
        },
        check_username: function () {
            var len = this.username.length;
            if (len < 5 || len > 20) {
                this.error_name = true;
                this.error_username_message = "请输入5-20个字符的用户";
            } else {
                this.error_name = false;
            }

            axios.get(this.host + '/usernames/' + this.username, {
                responseType: "json"
            }).then(response => {
                if (response.data.count > 0) {
                    this.error_name = true;
                    this.error_phone_message = "当前用户名已被注册";
                    return;
                } else {
                    this.error_name = false;
                }
            }).catch(error => {
                console.log(error.response.data);
            })
        },
        check_pwd: function () {
            var len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },
        check_cpwd: function () {
            if (this.password != this.password2) {
                this.error_check_password = true;
            } else {
                this.error_check_password = false;
            }
        },
        check_phone: function () {
            var re = /^1[345789]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone = true;
                this.error_phone_message = "您输入的手机号格式不正确";
                return;
            }

            axios.get(this.host + '/mobiles/' + this.mobile, {
                responseType: "json"
            }).then(response => {
                if (response.data.count > 0) {
                    this.error_name = true;
                    this.error_phone_message = "当前手机号已被注册";
                } else {
                    this.error_name = false;
                }
            }).catch(error => {
                console.log(error.response.data);
            })
        },
        check_image_code: function () {
            if (!this.image_code) {
                this.error_image_code = true;
                this.error_image_code_message = "请填写图片验证码";
            } else {
                this.error_image_code = false;
            }
        },
        check_sms_code: function () {
            if (!this.sms_code) {
                this.error_sms_code = true;
                this.error_sms_code_message = "请填写手机验证码"
            } else {
                this.error_sms_code = false;
            }
        },
        check_allow: function () {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        // 注册
        on_submit: function () {
            this.check_username();
            this.check_pwd();
            this.check_cpwd();
            this.check_phone();
            this.check_sms_code();
            this.check_allow();
            if (this.error_name == false && this.error_password == false && this.error_check_password == false
                && this.error_phone == false && this.error_sms_code == false && this.error_allow == false) {
                axios.post(this.host + '/register', {
                    username: this.username,
                    password: this.password,
                    password2: this.password2,
                    mobile: this.mobile,
                    sms_code: this.sms_code,
                    allow: this.allow.toString()
                }, {
                    responseType: 'json'
                })
                    .then(response => {
                        // 保存后端返回的token数据
                        localStorage.token = response.data.token;
                        localStorage.username = response.data.username;
                        localStorage.user_id = response.data.user_id;

                        location.href = '/index.html';
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            this.error_sms_code_message = '短信验证码错误';
                            this.error_sms_code = true;
                        } else {
                            console.log(error.response.data);
                        }
                    })
            }
        },
        send_sms: function () {
            if (this.send_flag === true) {
                return;
            }
            this.send_flag = true;
            this.check_phone();

            axios.get(this.host + "/sms_codes/" + this.mobile + "?text=" + this.image_code + "&image_code_id="
                + this.image_code_id, {
                responseType: "json"
            })
                .then(response => {
                    let num = 60;
                    let t = setInterval(() => {
                        if (num === 1) {
                            clearInterval();
                            this.sms_code_tip = "获取短信验证码";
                            this.send_flag = false;
                        } else {
                            num -= 1;
                            this.sms_code_tip = num + '秒';
                        }
                    }, 1000, 60)
                })
                .catch(error => {
                    if (error.response.status === 400) {
                        this.error_image_code_message = "图片验证码有误";
                        this.error_image_code = true;
                    } else {
                        console.log(error.response.data);
                    }
                    this.send_flag = false;
                });
        }
    }
});
