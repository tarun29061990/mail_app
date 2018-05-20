import { Component, OnInit, ViewChild }    from '@angular/core';
import { NgForm }               from "@angular/forms";
import { Router, ActivatedRoute }               from "@angular/router";

import {MailViewService} from "./mail-view.service";

@Component({
    moduleId: module.id,
    templateUrl: './mail-view.component.html',
    styleUrls: ['./mail-view.component.css']
})
export class MailViewComponent implements OnInit{
	
	public messageId:any;
	public message:any;
	public dataLoaded:boolean;

	constructor(private api: MailViewService, private router: Router, private route:ActivatedRoute){}
	
	ngOnInit(){
		const that = this;
		that.dataLoaded = false;
		that.route.params.subscribe(data=>{
     		that.messageId = data["id"];

     		that.api.getMessage(that.messageId).subscribe(data=>{
     			that.message = data[0]
     			that.dataLoaded = true;
     		}, err=>{});

     	});
	}
}