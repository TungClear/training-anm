import { AbstractControl } from '@angular/forms'

export function ageValidator(
  control: AbstractControl
): { [key: string]: any } | null {
  const valid = control.value > 0 && control.value <= 150
  return valid
    ? null
    : { invalidAge: { valid: false, value: control.value } }
}
