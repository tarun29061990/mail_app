import { NgModule }                   from '@angular/core';
import { RouterModule, Routes }       from '@angular/router';

import { LogInComponent }            from './login/login.component';
import { HomeComponent }            from './home/home.component';

const routes: Routes = [
    { path: 'login',           component: LogInComponent},
    { path: 'home',           component: HomeComponent},
    { path: '**',               redirectTo: 'login'}
];

@NgModule({
    imports: [ RouterModule.forRoot(routes) ],
    exports: [ RouterModule ]
})
export class AppRoutingModule {}
