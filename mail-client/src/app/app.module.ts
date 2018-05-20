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

import {ModalComponent} from './modal.component';

@NgModule({
  declarations: [
    AppComponent,
    LogInComponent,
    HomeComponent,
    ModalComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    LogInModule,
    FormsModule,
    HttpModule,
    HomeModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
