import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'bank-account-web';
  isAuth = null;

  constructor() {
    this.isAuth = localStorage.getItem('access_token')
  }

}
