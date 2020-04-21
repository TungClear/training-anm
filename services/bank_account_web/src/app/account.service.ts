import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators'
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Account } from 'src/models/account';
// import { ACCOUNTS_URL } from './constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { EnvService } from './env.service';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json',
    'Authorization': `Bearer ${localStorage.getItem('access_token') ? localStorage.getItem('access_token') : ''}`,
  })
};


@Injectable({
  providedIn: 'root'
})
export class AccountService {

  constructor(
    private http: HttpClient,
    private _snackBar: MatSnackBar,
    private env: EnvService
  ) {}

  ACCOUNTS_URL = this.env.apiUrl + '/accounts'

  getAccounts(query: any, orderBy, orderDirection, pageSize, pageIndex): Observable<any> {
    let url = `${this.ACCOUNTS_URL}`
    let params = {
      'account': JSON.stringify(query),
      'page_size': pageSize,
      'page_index': pageIndex,
      'order_by': orderBy,
      'order_direction': orderDirection
    }
    return this.http.get<any>(url, {
      ...httpOptions,
      params
    })
      .pipe(
        catchError(this.handleError)
      );
  }

  searchAccount(query: any, orderBy, orderDirection, pageSize, pageIndex): Observable<any> {
    let url =  `${this.ACCOUNTS_URL}/search`
    let postData = {
      'account': {...query},
      'page_size': pageSize,
      'page_index': pageIndex,
      'order_by': orderBy,
      'order_direction': orderDirection
    }
    return this.http.post<any>(url, postData, httpOptions)
      .pipe(
        catchError(this.handleError)
      );
  }

  addAccount(account: Account): Observable<any> {
    let url = this.ACCOUNTS_URL
    return this.http.post<any>(url, account, httpOptions)
      .pipe(
        catchError(this.handleError)
      );
  }

  getAccount(account_number): Observable<any> {
    let url = `${this.ACCOUNTS_URL}/${account_number}`
    return this.http.get<any>(url, httpOptions)
      .pipe(
        catchError(this.handleError)
      );
  }

  updateAccount(account: Account, account_number): Observable<any> {
    let url = `${this.ACCOUNTS_URL}/${account_number}`
    return this.http.put<any>(url, account, httpOptions)
      .pipe(
        catchError(this.handleError)
      );
  }

  deleteAccount(account_number): Observable<any> {
    let url =  `${this.ACCOUNTS_URL}/${account_number}`
    return this.http.delete<any>(url, httpOptions)
      .pipe(
        catchError(this.handleError)
      );
  }

  openSnackBar(message: string, action: string){
    this._snackBar.open(message, action, {
      duration: 2000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
    });
  }

  handleError = (error: HttpErrorResponse) => {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.log('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.log('error', error)
      console.log(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error.error}`);
      this.openSnackBar(`${error.status}:${error.error.error}`, 'Đóng')
    }
    // return an observable with a user-facing error message
    return throwError(
      'Something bad happened; please try again later.');
  };

}
