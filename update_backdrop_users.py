#!/usr/bin/env python
# encoding: utf-8
from stagecraft.apps.datasets.models import DataSet, BackdropUser


carers_allowance_weekly_claims_id = 21
carers_allowance_monthly_claims_id = 22
lpa_volumes_id = 12

carers_allowance_weekly_claims = [
    "catherine.mcwilliams@dwp.gsi.gov.uk",
    "adele.blundell@dwp.gsi.gov.uk",
    "kathryn.baxendale@dwp.gsi.gov.uk",
    "ian.middleton@dwp.gsi.gov.uk",
    "debbie.todd@dwp.gsi.gov.uk",
    "clifford.sheppard@digital.cabinet-office.gov.uk",
    "matt.harrington@digital.cabinet-office.gov.uk",
    "alan.penny@dwp.gsi.gov.uk",
    "rob.young@digital.cabinet-office.gov.uk",
    "lee.wardley@dwp.gsi.gov.uk",
    "greg.leighton@dwp.gsi.gov.uk",
    "nayeema.chowdhury@digital.cabinet-office.gov.uk",
    "tom.halloran@digital.cabinet-office.gov.uk",
    "mark.speakman@dwp.gsi.gov.uk",
    "jonathan.gilman@dwp.gsi.gov.uk"]

lpa_volumes = [
    "sarah.rees@publicguardian.gsi.gov.uk",
    "simon.manby@publicguardian.gsi.gov.uk",
    "zoe.gould1@publicguardian.gsi.gov.uk",
    "caroline.hufton2@publicguardian.gsi.gov.uk",
    "nayeema.chowdhury@digital.cabinet-office.gov.uk",
    "matt.harrington@digital.cabinet-office.gov.uk",
    "clifford.sheppard@digital.cabinet-office.gov.uk"]


def run_carers_allowance_claims():
    remove_all_monthly_claims_users()
    move_users_to_dataset(
        "carers_allowance_weekly_claims",
        "carers_allowance_transactions_by_channel",
        carers_allowance_weekly_claims)


def run_lpa_volumes():
    move_users_to_dataset(
        "lpa_volumes",
        "lasting_power_of_attorney_transactions_by_channel",
        lpa_volumes)


def remove_all_monthly_claims_users():
    # because there is no relation to users on the data set
    finished = False
    while not finished:
        try:
            monthly_claims = DataSet.objects.get(
                name='carers_allowance_monthly_claims')
            user = BackdropUser.objects.filter(
                data_sets__id=carers_allowance_monthly_claims_id).first()
            print("===================MONTHLY")
            print(user.data_sets.all())
            user.data_sets.remove(monthly_claims)
            print(user.data_sets.all())
        except AttributeError:
            finished = True


def move_users_to_dataset(old_dataset_name, new_dataset_name, users):
    old_dataset = DataSet.objects.get(name=old_dataset_name)
    new_dataset = DataSet.objects.get(name=new_dataset_name)
    for email in users:
        user = BackdropUser.objects.filter(email=email).first()
        print(user.data_sets.all())
        user.data_sets.remove(old_dataset)
        user.data_sets.add(new_dataset)
        print(user.data_sets.all())


if __name__ == '__main__':
    run_lpa_volumes()
    run_carers_allowance_claims()
