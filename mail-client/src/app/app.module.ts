import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppRoutingModule }           from './app-routing.module';
import { AppComponent } from './app.component';
import { LogInComponent }            from './login/login.component';
import { LogInModule }            from './login/login.module';

import { HomeComponent }            from './home/home.component';
import { HomeModule }            from './home/home.module';

import { MailViewComponent }            from './mailView/mail-view.component';
import { MailViewModule }            from './mailView/mail-view.module';

import {ModalComponent} from './modal.component';

@NgModule({
  declarations: [
    AppComponent,
    LogInComponent,
    HomeComponent,
    ModalComponent,
    MailViewComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    LogInModule,
    FormsModule,
    HttpModule,
    HomeModule,
    MailViewModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
