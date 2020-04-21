import { AccountSearch } from 'src/models/account-search';

export function formatDataQuery(account : AccountSearch) : any{
  for (let item in account) {
    if(item !== 'ageFrom' && item !== 'ageTo' && item !== 'account_number' && item!== 'balance') {
      account[item] = {'$regex':account[item], '$options': 'i'}
    } else{
      account[item] ? account[item] : delete account[item];
    }
    if(account['ageFrom'] && account['ageTo']){
      account['age'] = {
        '$gte': account['ageFrom'],
        '$lte': account['ageTo']
      }
      delete account['ageFrom'];
      delete account['ageTo'];
    } else if (account['ageFrom'] && !account['ageTo']){
      account['age'] = {
        '$gte': account['ageFrom'],
      }
      delete account['ageFrom'];
    }else if (!account['ageFrom'] && account['ageTo']){
      account['age'] = {
        '$lte': account['ageTo']
      }
      delete account['ageTo'];
    }
  }
  return account
}

export function validateEmail(email : string) {
  var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}
