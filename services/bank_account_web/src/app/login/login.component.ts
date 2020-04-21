import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';

import { UserService } from '../user.service';
import { User } from 'src/models/user';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;

  account_validation_messages = {
    'username': [
      { type: 'required', message: 'Username is required' },
    ],
    'password': [
      { type: 'required', message: 'Password is required' },
    ]
  }

  constructor(
    private userService: UserService,
    private _snackBar: MatSnackBar,
    private formBuilder: FormBuilder
  ) { }

  ngOnInit() {
    this.createForms();
  }

  createForms(): void {
    // user links form validations
    this.loginForm = this.formBuilder.group({
      username: new FormControl('', Validators.compose([
        Validators.required
      ])),
      password: new FormControl('', Validators.compose([
        Validators.required,
      ]))
    })
  }

  onSubmitAccountDetails(value){
    this.userService.login(new User(value.username, value.password))
      .subscribe(response => {
          const { success } = response
          if(success === 1){
            localStorage.setItem('access_token', response.access_token)
            localStorage.setItem('role', response.role)
            window.location.reload();
          }else{
            this.openSnackBar(response.message, 'Đóng')
          }
        }
      );
  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 2000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
    });
  }

}
