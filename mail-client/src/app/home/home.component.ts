import { Component, OnInit, ViewChild }    from '@angular/core';
import { NgForm }               from "@angular/forms";
import { Router }               from "@angular/router";

import {HomeService} from "./home.service";

@Component({
    moduleId: module.id,
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit{
	public email:any;
	public password:any;

	public toEmail:any;
	public subject:any;
	public body:any;
	public senderEmail:any;
	public senderId:any;

	public placeholderName:any;
	public mails:any;

	public showLoader:boolean;

	@ViewChild('composeModel')composeModel: any;

	constructor(private api: HomeService, private router: Router){}
	
	ngOnInit(){
		const that = this;
		that.mails = [];
		that.showLoader = false;

		let user = JSON.parse(localStorage.getItem('current_user'));
		that.senderEmail = user["email"];
		that.senderId = user["id"];

		this.getPlaceholderMails('inbox');
	}

	openComposeBox(){
		this.composeModel.show();
	}

	hideComposeBox(){
		this.composeModel.hide();
	}

	sendMail(){
		const that = this;


		let mail_dict = {
			"body": that.body,
			"subject": that.subject,
			"recipient_email": that.toEmail,
			"sender_email":that.senderEmail
		}

		that.api.sendMail(mail_dict).subscribe(data=>{
			console.log('Mail sent');
			that.getPlaceholderMails('inbox');
			that.hideComposeBox();
		}, err=>{})
	}

	getPlaceholderMails(placeholderName){
		const that = this;

		that.placeholderName = placeholderName;

		that.showLoader = true;
		that.api.getPlaceholderMails(that.senderId, placeholderName).subscribe(data=>{
			that.showLoader = false;
			that.mails = data.mp;
		}, err=>{});
	}

	saveToDrafts(){
		const that = this;

		let mail_dict = {
			"body": that.body,
			"subject": that.subject,
			"sender_email":that.senderEmail
		}
		that.showLoader = true;
		that.api.saveToDrafts(mail_dict).subscribe(data=>{

			that.showLoader = false;
			that.hideComposeBox();

		}, err=>{});
	}

	trashIt(mail){
		const that = this;

		that.showLoader = true;
		that.api.trashIt(mail.id).subscribe(data=>{
			
			that.showLoader = false;
			that.getPlaceholderMails('inbox');
		}, err=>{});
	}
}