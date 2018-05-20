import { Component, OnInit }    from '@angular/core';
import { NgForm }               from "@angular/forms";
import { Router }               from "@angular/router";

import {LogInService} from "./login.service";

@Component({
    moduleId: module.id,
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LogInComponent{
	public email:any;
	public password:any;

	constructor(private api: LogInService, private router: Router){}

	login(){
		const that = this;

		that.api.login(that.email, that.password).subscribe(data=>{
			if(data.length){
				localStorage.setItem('current_user',JSON.stringify({'email':that.email,'id':data[0].id}));
				that.router.navigateByUrl('/home');
			}
		}, err=>{});
	}
}