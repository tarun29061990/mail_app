import { Injectable } from '@angular/core';
import { Http, Request, RequestMethod, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { environment } from '../../environments/environment';

import 'rxjs/add/operator/map';

@Injectable()
export class LogInService {
    AUTH_URL: any;
    API_URL: any;
    auth_token: string;
    constructor(private http: Http) {
        
        
        if (environment.envName === 'dev') {
            this.AUTH_URL = '';
            this.API_URL = '';
        } else if (environment.envName === 'prod') {
            this.AUTH_URL = '//sample.backend.grexter.in';
            this.API_URL = '//sample.backend.grexter.in';
        } else if (environment.envName === 'local') {
            this.AUTH_URL = '//localhost:4000';
            this.API_URL = '//localhost:4000';
        } else if (environment.envName === 'stage') {
            this.AUTH_URL = '';
            this.API_URL = '';
        }
    }
    private sendRequest(verb: RequestMethod, path: string, body: any, auth: boolean = false, header: any = {}): Observable<any> {
        let request = new Request({
            method: verb,
            url: this.API_URL + path,
            body: body
        });
        if (auth && this.auth_token) {
            request.headers.set('Authorization', `Bearer ${this.auth_token}`)
        }

        if (header.name && header.value) {
            request.headers.set(header.name, header.value);
        }

        return this.http.request(request).map(response => response.json());

    }
    login(email:any, password:any): Observable<any> {
        let dict = {
            'email':email,
            'password':password
        }
        return this.sendRequest(RequestMethod.Post, '/login', dict, false);
    }
}