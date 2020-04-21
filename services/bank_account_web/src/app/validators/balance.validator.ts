import { AbstractControl } from '@angular/forms'

export function balanceValidator(
  control: AbstractControl
): { [key: string]: any } | null {
  const valid = control.value >= 0
  return valid
    ? null
    : { invalidBalance: { valid: false, value: control.value } }
}
