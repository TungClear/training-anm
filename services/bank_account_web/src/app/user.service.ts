import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators'
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { User } from '../models/user';
import { AUTH_URL } from './constants'
import { EnvService } from './env.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  login (user: User): Observable<any> {
    let url = `${this.env.apiUrl}/login`
    return this.http.post<any>(url, user)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.log('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.log(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // return an observable with a user-facing error message
    return throwError(
      'Something bad happened; please try again later.');
  };

  constructor(
    private http: HttpClient,
    private env: EnvService
  ) { }
}
