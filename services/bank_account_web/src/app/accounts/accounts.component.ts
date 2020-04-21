import { Component, OnInit, ViewChild } from '@angular/core';
import * as _ from 'lodash';
import { Account } from '../../models/account';
import { AccountSearch } from 'src/models/account-search';
import { AccountService } from '../account.service';
import { DialogComponent } from '../dialog/dialog.component';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { PageEvent } from '@angular/material/paginator';
import { Sort } from '@angular/material/sort';

import { formatDataQuery } from '../utils';

@Component({
  selector: 'app-accounts',
  templateUrl: './accounts.component.html',
  styleUrls: ['./accounts.component.css']
})
export class AccountsComponent implements OnInit {

  public accounts: Account[];
  public account: Account = new Account();
  public accountSearch: AccountSearch = new AccountSearch();
  public displayedColumns: string[];
  public dataSource = new MatTableDataSource<Account>();
  public isAdmin : boolean ;
  public formMode: string;
  public gender : string[] = ['Both', 'M', 'F'];
  public loading : boolean;

  public total:number;
  public pageSize:number = 10;
  public pageIndex:number = 0;
  public orderBy:string = 'account_number';
  public orderDirection:number = -1;//1 #ascending, -1 #descending
  public pageEvent: PageEvent;

  public dialogRef: any;

  public isAdvanceSearch: boolean = false;

  @ViewChild(MatPaginator) paginator: MatPaginator;

  constructor(
    public dialog: MatDialog,
    private accountService : AccountService,
    private _snackBar: MatSnackBar
  ) {
    this.isAdmin = localStorage.getItem('role') === '10';
    this.displayedColumns = ['account_number', 'firstname', 'lastname', 'balance', 'age', 'gender', 'address', 'employer', 'email', 'city', 'state', 'action']
  }

  ngOnInit() {
    this.searchAccount(null, false);
  }

  onClickViewAccount(account: Account) : void {
    this.account = account;
    this.openDialog('view')
  }

  onClickAddAccount(): void {
    this.account = new Account();
    this.openDialog('add')
  }
  onClickEditAccount(account: Account): void {
    this.account = account;
    this.openDialog('edit')
  }
  onClickDeleteAccount(account_number): void {
    this.deleteAccount(account_number)
  }

  onClickLogout(): void {
    localStorage.clear();
    window.location.reload();
  }

  addAccount = (account: Account) => {
    this.accountService.addAccount(account).subscribe(response => {
      const { success, message } = response
      if(success){
        this.searchAccount(null, true);
        this.dialogRef.close()
      }
      this.openSnackBar(message, 'Close')
    })
  }

  updateAccount = (account: Account, account_number: any) => {
    this.accountService.updateAccount(account, account_number).subscribe(response => {
      const { success, message } = response
      if(success){
        this.searchAccount(null, true);
        this.dialogRef.close()
      }
      this.openSnackBar(message, 'Close')
    })
  }

  deleteAccount(account_number: number): void {
    this.accountService.deleteAccount(account_number).subscribe(response => {
      const { success, message } = response
      if(success){
        this.searchAccount(null, true);
      }
      this.openSnackBar(message, 'Close')
    })
  }

  searchAccount(event?:PageEvent, withPaging?: Boolean): void {
    // let query = JSON.parse(JSON.stringify(this.accountSearch));
    if(!this.checkValidAgeFromTo()){
      this.openSnackBar('Age from must less than to', 'Close')
      return;
    }
    let query = _.clone(this.accountSearch)
    if(query.gender && query.gender === 'Both'){
      delete query.gender
    }
    query = formatDataQuery(query)
    this.loading = true;
    this.pageSize = event ? event.pageSize : this.pageSize;
    if(withPaging){
      this.pageIndex = event ? event.pageIndex : this.pageIndex;
    }else{
      this.pageIndex = 0;
    }
    this.accountService.getAccounts(query, this.orderBy, this.orderDirection, this.pageSize, this.pageIndex).subscribe(response => {
      const { success, data, total, message } = response
      if(success){
        this.accounts = data;
        this.dataSource = new MatTableDataSource<Account>(data);
        this.total = total;
      }else{
        this.openSnackBar(message, 'Close')
      }
      this.loading = false;
    })
  }

  sortAccount(event: Sort, withPaging?: Boolean) {
    if(!this.checkValidAgeFromTo()){
      this.openSnackBar('Age from must less than to', 'Close')
      return;
    }
    let query = _.clone(this.accountSearch)
    if(query.gender && query.gender === 'Both'){
      delete query.gender
    }
    query = formatDataQuery(query)
    this.loading = true;
    this.orderBy = event ? event.active : this.orderBy;
    this.orderDirection = event ? event.direction === 'asc' ? 1 : -1 : this.orderDirection;
    if(!withPaging){
      this.pageIndex = 0;
    }
    this.accountService.getAccounts(query, this.orderBy, this.orderDirection, this.pageSize, this.pageIndex).subscribe(response => {
      const { success, data, total, message } = response
      if(success){
        this.accounts = data;
        this.dataSource = new MatTableDataSource<Account>(data);
        this.total = total;
      }else{
        this.openSnackBar(message, 'Close')
      }
      this.loading = false;
    })
  }

  openDialog(formMode): void {
    this.dialogRef = this.dialog.open(DialogComponent, {
      width: '50%',
      data: {
        account: {...this.account},
        formMode,
        addAccount: this.addAccount,
        updateAccount: this.updateAccount
      },
      disableClose: true,
    });
    // dialogRef.afterClosed().subscribe(result => {
    //   if(result){
    //     if(formMode === 'add'){
    //       this.addAccount(result)
    //     }else{
    //       this.updateAccount(result, this.account.account_number)
    //     }
    //   }
    // });
  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 2000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
    });
  }

  onClickAdvanceSearch() {
    this.isAdvanceSearch = !this.isAdvanceSearch
    if(!this.isAdvanceSearch){
      this.resetFieldAdvanceSearch()
      this.searchAccount(null, true)
    }
  }

  resetSearch(){
    this.accountSearch = new AccountSearch()
    this.searchAccount(null, false)
  }

  resetFieldAdvanceSearch() {
    this.accountSearch.ageFrom = null;
    this.accountSearch.ageTo = null;
    this.accountSearch.email = '';
    this.accountSearch.gender = '';
    this.accountSearch.balance = null;
    this.accountSearch.address = '';
    this.accountSearch.employer = '';
    this.accountSearch.city = '';
    this.accountSearch.state = '';
  }

  checkValidAgeFromTo() {
    if(this.accountSearch.ageFrom && this.accountSearch.ageTo){
      if(this.accountSearch.ageFrom > this.accountSearch.ageTo){
        return false
      }
    }
    return true
  }

}
