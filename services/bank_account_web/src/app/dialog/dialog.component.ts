import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ageValidator } from '../validators/age.validator'
import { balanceValidator } from '../validators/balance.validator'

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.css']
})
export class DialogComponent implements OnInit {

  userDetailsForm: FormGroup;

  genders : string[] = ['M', 'F'];

  validation_messages = {
    'account_number': [
      { type: 'required', message: 'Account number is required' },
      { type: 'pattern', message: 'Account number must be numbers' },
    ],
    'firstname': [
      { type: 'required', message: 'First name is required' },
      { type: 'maxlength', message: 'First name cannot be more than 100 characters' },
    ],
    'lastname': [
      { type: 'required', message: 'Last name is required' },
      { type: 'maxlength', message: 'Last name cannot be more than 100 characters' },
    ],
    'balance': [
      { type: 'required', message: 'Balance is required' },
      { type: 'pattern', message: 'Balance must be numbers and greater than 0' },
      // { type: 'validBalance', message: 'Balance must greater or equal than 0' }
    ],
    'age': [
      { type: 'required', message: 'Age is required' },
      { type: 'pattern', message: 'Age must be numbers' },
      { type: 'invalidAge', message: 'Age must between 1 and 150' }
    ],
    'gender': [
      { type: 'required', message: 'Please select your gender' },
    ],
    'address': [
      { type: 'required', message: 'Address is required' },
      { type: 'maxlength', message: 'Address cannot be more than 100 characters' },
    ],
    'employer': [
      { type: 'required', message: 'Employer is required' },
      { type: 'maxlength', message: 'Employer cannot be more than 100 characters' },
    ],
    'email': [
      { type: 'required', message: 'Email is required' },
      { type: 'pattern', message: 'Enter a valid email' }
    ],
    'city': [
      { type: 'required', message: 'City is required' },
      { type: 'maxlength', message: 'City cannot be more than 50 characters' },
    ],
    'state': [
      { type: 'required', message: 'City is required' },
      { type: 'maxlength', message: 'City cannot be more than 50 characters' },
    ]
  };

  constructor(
    public dialogRef: MatDialogRef<DialogComponent>,
    private formBuilder: FormBuilder,
    @Inject(MAT_DIALOG_DATA) public data: any,
  ) {
    // this.account = Object.assign({}, data.account);
  }

  ngOnInit() {
    this.createForms();
  }

  createForms() {
    let { account, formMode } = this.data
    this.userDetailsForm = this.formBuilder.group({
      account_number: new FormControl({value: account.account_number, disabled: formMode !== 'add'}, Validators.compose([
        Validators.required,
        Validators.pattern(/^\d+$/)
      ])),
      firstname: new FormControl({value: account.firstname, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.maxLength(100),
      ])),
      lastname: new FormControl({value: account.lastname, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.maxLength(100),
      ])),
      balance: new FormControl({value: account.balance, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.pattern(/^\d+$/),
        // balanceValidator,
      ])),
      age: new FormControl({value: account.age, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.pattern(/^\d+$/),
        ageValidator,
      ])),
      gender: new FormControl({value: account.gender, disabled: formMode === 'view'}, Validators.required),
      address: new FormControl({value: account.address, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.maxLength(100),
      ])),
      employer: new FormControl({value: account.employer, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.maxLength(100),
      ])),
      email: new FormControl({value: account.email, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.pattern('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$')
      ])),
      city: new FormControl({value: account.city, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.maxLength(50),
      ])),
      state: new FormControl({value: account.state, disabled: formMode === 'view'}, Validators.compose([
        Validators.required,
        Validators.maxLength(50),
      ])),
    });
  }

  onClickFormCancel() : void {
    this.dialogRef.close();
  }

  onSubmitUserDetails(){
    let { account, formMode, addAccount, updateAccount } = this.data
    let result = 1;
    if(formMode === 'add'){
      addAccount(this.userDetailsForm.value)
    }else{
      updateAccount(this.userDetailsForm.value, account.account_number)
    }
  }
}
