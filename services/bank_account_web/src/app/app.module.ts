import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { EnvServiceProvider } from './env.service.provider';
import { HttpClientModule } from '@angular/common/http';

import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatDialogModule } from '@angular/material/dialog';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSortModule } from '@angular/material/sort';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { AccountsComponent } from './accounts/accounts.component';
import { DialogComponent } from './dialog/dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AccountsComponent,
    DialogComponent
  ],
  entryComponents: [DialogComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatIconModule,
    MatSelectModule,
    MatInputModule,
    MatTableModule,
    MatPaginatorModule,
    MatButtonModule,
    MatMenuModule,
    MatSnackBarModule,
    MatToolbarModule,
    MatProgressBarModule,
    MatGridListModule,
    MatDialogModule,
    MatTooltipModule,
    MatSortModule
  ],
  providers: [EnvServiceProvider],
  bootstrap: [AppComponent]
})
export class AppModule { }
